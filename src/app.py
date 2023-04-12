from flask import Flask, render_template, redirect, request, jsonify
from config import config   
import os
import mysql.connector
app = Flask(__name__)

print(os.environ['HOST'])

@app.route('/')
def index():
    return redirect('/auth')

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        try:
            connection = mysql.connector.connect(
                host=os.environ['HOST'],
                user=os.environ['USER'],
                password=os.environ['PASSWORD'],
                database=os.environ['users']
            )
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            results = cursor.excecute(query)
            print(results)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
        return jsonify(request.form)



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run() 