from entities import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE name = '{user.username}' AND password = '{user.password}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            print(res)
            cursor.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
            
        except Exception as err:
            raise Exception(err)
    @classmethod 
    def get_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id WHERE user_id={id};"
            cursor.execute(sql)
            res = cursor.fetchone()
            cursor.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4])
        except Exception as err:
            raise Exception(err)
    @classmethod
    def get_all(self, db):
        try:
            cursor = db.cursor()
            sql = f"SELECT user_id, name, id_role, password, role FROM users JOIN roles ON users.id_role=roles.rol_id;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def insert_one(self, connection, user):
        try:
            cursor = connection.cursor()
            sql = f"INSERT INTO users (name, id_role, password) VALUES ('{user.username}', {user.role}, '{user.password}');"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
        except Exception as err:
            raise Exception(err)
    @classmethod
    def delete_one(self, connection, id):
        try:
            cursor = connection.cursor()
            sql = f"DELETE FROM users WHERE user_id={id};"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
        except Exception as err:
            raise Exception(err)
        
    @classmethod
    def update_one(self, connection, user):
        try:
            cursor = connection.cursor()
            sql = f"UPDATE users SET name='{user.username}', id_role={user.role}, password='{user.password}' WHERE user_id={user.id};"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
        except Exception as err:
            raise Exception(err)