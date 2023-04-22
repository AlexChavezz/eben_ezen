import os
import mysql.connector
from flask import Response


class ModelProduct():
    @classmethod
    def get_all(self, connection):
        try:
            cursor = connection.cursor()
            sql = "SELECT * FROM products;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as err:
            raise Exception(err)
    @classmethod
    def save(self, connection, product):
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO products (name, marca, price, stock, description) VALUES (%s, %s, %s, %s, %s);', (product.name, product.marca, product.price, product.stock, product.description))
            cursor.close()
            return Response('Product saved', 200)
        except Exception as e:
            raise Exception(e)
    @classmethod
    def delete_by_id(self, id):
        try:
            cursor = self.get_connection().cursor()
            cursor.excecute('DELETE FROM products WHERE product_id = %s', (id))
            cursor.close()
            return Response('Product deleted', 200)
        except Exception as e:
            raise Exception(e)
        
        
        
        