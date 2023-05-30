from flask import Response
from models.DatabaseConnection import DatabaseConnection
from entities import Product

class ModelProduct(DatabaseConnection):
    @classmethod
    def get_all(self):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = "SELECT * FROM products;"
            cursor.execute(sql)
            res = cursor.fetchall()
            super().destroy_conection(connection, cursor)
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def save(self, product):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"INSERT INTO products (name, marca, price, stock, description) VALUES ('{product.name}', '{product.marca}', {product.price}, {product.stock}, '{product.description}');"
            cursor.execute(sql)
            connection.commit()
            super().destroy_conection(connection, cursor)
            return Response('Product saved', 200)
        except Exception as e:
            raise Exception(e)
    @classmethod
    def get_by_id(self, id):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            sql = f"SELECT * FROM products WHERE product_id = {id};"
            cursor.execute(sql)
            res = cursor.fetchone()
            super().destroy_conection(connection, cursor)
            return Product(res[0], res[1], res[2], res[3], res[4], res[5])
        except Exception as e:
            raise Exception(e)
    @classmethod 
    def update_one(self, product):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            cursor.execute('UPDATE products SET name = %s, marca = %s, price = %s, stock = %s, description = %s WHERE product_id = %s', (product.name, product.marca, product.price, product.stock, product.description, product.product_id))
            connection.commit()
            super().destroy_conection(connection, cursor)
            return Response('Product updated', 200)
        except Exception as e:
            raise Exception(e)
        
        