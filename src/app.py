from flask import Flask, render_template, redirect, request, jsonify, flash
from config import config   
from entities import User, DefUser, Product
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct
import mysql.connector
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

csrf = CSRFProtect()
connection = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    password=os.environ['PASSWORD'],
    database=os.environ['DATABASE']
)

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(connection, id)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if(current_user.is_authenticated):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        try:
            user = User(None, request.form['username'], None, request.form['password'], None)
            logged_user = ModelUser.login(connection, user)
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
    if(current_user.role != 'employed'):
        return redirect('/dashboard')
    return render_template('/salespoint/index.html')

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
    #Retrive all products from database
    if request.method == 'GET':
        users = ModelUser.get_all(connection)
        return render_template('/dashboard/users/users.html', users=users)
    else:
        try:
            print(request.form)
            # if request.form['password'] != request.form['confirm_password']:
            #     flash('Passwords do not match')
            #     return 
            user = DefUser(None, request.form['username'], request.form['role'], request.form['password'])
            ModelUser.insert_one(connection, user)
            return redirect('/dashboard/users')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})
    

@app.route('/dashboard/products', methods=['POST', 'GET'])
# @login_required
def products():
    if isNotAdmin():
        return redirect('/salespoint')
    if request.method == 'GET':
        products = ModelProduct.get_all(connection)
        return render_template('/dashboard/products/products.html', products=products)
    if request.method == 'POST':
        # save product
        try:
            print(request.form)
            product = Product(None, request.form['name'], request.form['marca'], request.form['price'], request.form['stock'], request.form['description'])
            ModelProduct.save(connection, product)
            return redirect('/dashboard/products')
        except Exception as err:
            print(err)
            return jsonify({'ok': False, 'error':str(err)})
    

def isNotAdmin():
    if current_user.role != 'admin':
        return True
    return False
    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run() 