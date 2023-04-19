class ModelProduct:
    def get_all(connection):
        try:
            cursor = connection.cursor()
            sql = f"SELECT * FROM products;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as err:
            raise Exception(err)        