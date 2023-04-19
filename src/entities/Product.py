import os
import mysql.connector
from flask import Response
class Product():
    def __init__ (self, product_id, name, marca, price, stock, description) -> None:
        self.product_id = product_id
        self.name = name
        self.marca = marca
        self.price = price
        self.stock = stock
        self.description = description
    @classmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['DATABASE'])
    @classmethod
    def save(self):
        try:
            cursor = self.get_connection().cursor()
            cursor.excecute('INSERT INTO products (name, marca, price, stock, description) VALUES (%s, %s, %s, %s, %s)', (self.name, self.marca, self.price, self.stock, self.description))
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
    @classmethod
    def get_all(self, db):
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM products;"
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as err:
            raise Exception(err)
        
        
        
        