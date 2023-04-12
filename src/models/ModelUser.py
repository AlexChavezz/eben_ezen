from entities import User

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.cursor()
            sql = f"SELECT * FROM users WHERE name = '{user.username}' AND password = '{user.password}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            print (res)
            cursor.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], res[3])
            
        except Exception as err:
            raise Exception(err)
    @classmethod 
    def get_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = f"SELECT * FROM users WHERE user_id = '{id}';"
            cursor.execute(sql)
            res = cursor.fetchone()
            cursor.close()
            if res == None:
                return None
            else:
                return User(res[0], res[1], res[2], None)
        except Exception as err:
            raise Exception(err)