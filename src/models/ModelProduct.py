from flask import Response
from entities import Product
import mysql.connector
import os

class ModelProduct():
    @classmethod
    def get_connection(self):
        return mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['database']
        )
    @classmethod
    def get_all(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM products;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            connection.close()
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def save(self, product):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"INSERT INTO products (name, marca, price, stock, description) VALUES ('{product.name}', '{product.marca}', {product.price}, {product.stock}, '{product.description}');"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
            return Response('Product saved', 200)
        except Exception as e:
            raise Exception(e)
    @classmethod
    def get_by_id(self, id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql = f"SELECT * FROM products WHERE product_id = {id};"
            cursor.execute(sql)
            res = cursor.fetchone()
            cursor.close()
            connection.close()
            return Product(res[0], res[1], res[2], res[3], res[4], res[5])
        except Exception as e:
            raise Exception(e)
    @classmethod 
    def update_one(self, product):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE products SET name = %s, marca = %s, price = %s, stock = %s, description = %s WHERE product_id = %s', (product.name, product.marca, product.price, product.stock, product.description, product.product_id))
            connection.commit()
            cursor.close()
            connection.close()
            return Response('Product updated', 200)
        except Exception as e:
            raise Exception(e)
        
        