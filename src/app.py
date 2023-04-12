from flask import Flask, render_template, redirect, request, jsonify, flash
from config import config   
from entities import User
from models.ModelUser import ModelUser
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
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        try:
            
            user = User(None, request.form['username'], None, request.form['password'])
            logged_user = ModelUser.login(connection, user)
            print(logged_user)
            if logged_user == None:
                flash('Invalid credentials')
                return redirect('/login')
            else:
                if logged_user.password:
                    login_user(logged_user)
                    return redirect('/home')
                else:
                    flash('Invalid credentials')
                    return redirect('/login')
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'error': str(e)})  

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/home')
@login_required
def home():
    return render_template('/home/home.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run() 