from models.DatabaseConnection import DatabaseConnection
from entities import User
from flask import Response

class ModelUser(DatabaseConnection):
    @classmethod
    def login(self, user):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"SELECT user_id, username, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE username = '{user.username}' AND password = '{user.password}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            super().destroy_conection(connection, cursor)
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
            
        except Exception as err:
            raise Exception(err)
    @classmethod 
    def get_by_id(self, id):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"SELECT user_id, username, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE user_id={id};"
            cursor.execute(sql)
            res = cursor.fetchone()
            super().destroy_conection(connection, cursor)
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
        except Exception as err:
            raise Exception(err)
    @classmethod
    def get_all(self):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"SELECT user_id, username, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id;"
            cursor.execute(sql)
            res = cursor.fetchall()
            super().destroy_conection(connection, cursor)
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def insert_one(self, user):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"INSERT INTO users (username, id_role, password) VALUES ('{user.username}', {user.id_role}, '{user.password}');"
            cursor.execute(sql)
            connection.commit()
            super().destroy_conection(connection, cursor)
        except Exception as err:
            raise Exception(err)
    @classmethod
    def delete_one(self, id):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"DELETE FROM users WHERE user_id={id};"
            cursor.execute(sql)
            connection.commit()
            super().destroy_conection(connection, cursor)
            return Response('User deleted', 200)
        except Exception as err:
            raise Exception(err)
        
    @classmethod
    def update_one(self, user):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"UPDATE users SET username='{user.username}', id_role={user.id_role}, password='{user.password}' WHERE user_id={user.id};"
            cursor.execute(sql)
            connection.commit()
            super().destroy_conection(connection, cursor)
        except Exception as err:
            raise Exception(err)