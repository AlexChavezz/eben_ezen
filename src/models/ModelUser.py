from entities import User
from flask import Response
import os
import mysql.connector


class ModelUser():
    @classmethod
    def get_connection(self):
        return mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE']
        )
    @classmethod
    def login(self, user):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE name = '{user.username}' AND password = '{user.password}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            print(res)
            cursor.close()
            connection.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
            
        except Exception as err:
            raise Exception(err)
    @classmethod 
    def get_by_id(self, id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE user_id={id};"
            cursor.execute(sql)
            res = cursor.fetchone()
            cursor.close()
            connection.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
        except Exception as err:
            raise Exception(err)
    @classmethod
    def get_all(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            connection.close()
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def insert_one(self, user):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"INSERT INTO users (name, id_role, password) VALUES ('{user.username}', {user.id_role}, '{user.password}');"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as err:
            raise Exception(err)
    @classmethod
    def delete_one(self, id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"DELETE FROM users WHERE user_id={id};"
            cursor.execute(sql)
            cursor.close()
            connection.commit()
            connection.close()
            return Response('User deleted', 200)
        except Exception as err:
            raise Exception(err)
        
    @classmethod
    def update_one(self, user):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"UPDATE users SET name='{user.username}', id_role={user.id_role}, password='{user.password}' WHERE user_id={user.id};"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as err:
            raise Exception(err)