from flask import Flask, render_template, redirect, request, jsonify, flash
from config import config
from entities import User, DefUser, Product, Sale
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct
from models.ModelSale import ModelSale
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (current_user.is_authenticated):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        try:
            user = User(None, request.form['username'],
                        None, request.form['password'], None)
            logged_user = ModelUser.login(user)
            if logged_user == None:
                flash('Invalid credentials')
                return redirect('/login')
            login_user(logged_user)
            if current_user.role == 'admin':
                return redirect('/dashboard')
            if current_user.role == 'employed':
                return redirect('/salespoint')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/salespoint')
@login_required
def salespoint():
    if (current_user.role != 'employed'):
        return redirect('/dashboard')
    return render_template('/salespoint/index.html')

@app.route('/sales/add_sale', methods=['POST'])
@csrf.exempt
def post_sale():
    try:
        request_data = request.get_json()
        sale_object = Sale(None, request_data['saleDate'], total_price=request_data['total'], id_user=current_user.id)
        sale_id = ModelSale.register_sale(sale_object)
        ModelSale.insert_into_sale_product(request_data['products'], sale_id)
        ModelSale.update_product_stock(request_data['products'])
        return jsonify({"status":"done!"})
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'error': str(e)})

@app.route('/products/get_products')
def get_products():
    products = ModelProduct.get_all()
    return jsonify({'ok': True, 'products': products})
    
@app.route('/dashboard')
@login_required
def dashboard():
    if isNotAdmin():
        return redirect('/salespoint')
    return redirect('/dashboard/users')


@app.route('/dashboard/users', methods=['POST', 'GET'])
@login_required
def users():
    if isNotAdmin():
        return redirect('/salespoint')
    # Retrive all products from database
    if request.method == 'GET':
        users = ModelUser.get_all()
        return render_template('/dashboard/users/users.html', users=users)
    else:
        try:
            user = DefUser(
                None, request.form['username'], request.form['role'], request.form['password'])
            ModelUser.insert_one(user)
            return redirect('/dashboard/users')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})


@app.route('/dashboard/products', methods=['POST', 'GET'])
@login_required
def products():
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'GET':
        products = ModelProduct.get_all()
        return render_template('/dashboard/products/products.html', products=products)
    elif request.method == 'POST':
        # save product
        try:
            print(request.form)
            product = Product(None, request.form['name'], request.form['marca'],
                              request.form['price'], request.form['stock'], request.form['description'])
            ModelProduct.save(product)
            return redirect('/dashboard/products')
        except Exception as err:
            print(err)
            return jsonify({'ok': False, 'error': str(err)})

@app.route('/dashboard/products/update/<id>', methods=['GET', 'POST'])
@login_required
def update_products(id):
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'POST':
        product = Product(id, request.form['name'], request.form['marca'],
        request.form['price'], request.form['stock'], request.form['description'])
        ModelProduct.update_one(product)
        return redirect('/dashboard/products')
    if request.method == 'GET':
        product = ModelProduct.get_by_id(id)
        return render_template('/dashboard/products/editform.html', product=product)


@app.route('/dashboard/products/create', methods=['POST', 'GET'])
@login_required
def create_products():
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'GET':
        return render_template('/dashboard/products/newProductForm.html')
    elif request.method == 'POST':
        try:
            product = Product(None, request.form['name'], request.form['marca'],
                              request.form['price'], request.form['stock'], request.form['description'])
            ModelProduct.save(product)
            return redirect('/dashboard/products')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})


@app.route('/dashboard/users/create', methods=['GET', 'POST'])
@login_required
def create_users():
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'POST':
        try:
            user = DefUser(None, request.form['username'], request.form['role'], request.form['password'])
            ModelUser.insert_one(user)
            return redirect('/dashboard/users')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})
    elif request.method == 'GET':
        return render_template('/dashboard/users/newUserForm.html')

@app.route('/dashboard/users/update/<id>', methods=['GET', 'POST'])
@login_required
def update_users(id):
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'POST':
        print(request.form)
        user = DefUser(id, request.form['username'], request.form['id_role'], request.form['password'])
        ModelUser.update_one(user)
        return redirect('/dashboard/users')
    if request.method == 'GET':
        user = ModelUser.get_by_id(id)
        return render_template('/dashboard/users/editUserForm.html', user=user)

@app.route('/dashboard/users/deleteone/<id>', methods=['GET'])
@login_required
def delete_user(id):
    if isNotAdmin():
        return redirect('/salespoint')
    ModelUser.delete_one(id)
    return redirect('/dashboard/users')

def isNotAdmin():
    if current_user.role != 'admin':
        return True
    return False


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run()
