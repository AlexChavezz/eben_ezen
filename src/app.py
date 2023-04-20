from flask import Flask, render_template, redirect, request, jsonify, flash
from config import config   
from entities import User
from models.ModelUser import ModelUser
from models.ModelProduct import ModelProduct
import mysql.connector
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

# csrf = CSRFProtect()

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
    if request.method == 'POST':
        try:
            print(request.form)
            user = User(None, request.form['username'], request.form['email'], request.form['password'], request.form['role'])
            ModelUser.insert_one(connection, user)
            return redirect('/dashboard/users')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})
    users = ModelUser.get_all(connection)
    return render_template('/dashboard/users/users.html', users=users)

@app.route('/dashboard/products')
# @login_required
def products():
    if isNotAdmin():
        return redirect('/salespoint')
    return render_template('/dashboard/products/products.html')


def isNotAdmin():
    if current_user.role != 'admin':
        return True
    return False

"""
    @ROUTES for imlpement CRUD operations
"""

# @app.route('/api/v1/:users', methods=['POST'])

# @app.route('/api/v1/users/register', methods=['POST'])
# @login_required
# def register():
#     try:
#         print(request.form)
#         # user = User(None, request.form['username'], request.form['email'], request.form['password'], request.form['role'])
#         # ModelUser.insert_one(connection, user)
#         return redirect('/dashboard')
#     except Exception as e:
#         print(e)
#         return jsonify({'ok': False, 'error': str(e)})
    
@app.route('/api/v1/users/delete/<int:id>')
@login_required
def delete_user(id):
    if isNotAdmin():
        return redirect('/salespoint')
    ModelUser.delete_one(connection, id)
    return redirect('/dashboard/users')


if __name__ == '__main__':
    app.config.from_object(config['development'])
    # csrf.init_app(app)
    app.run() 