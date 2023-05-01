import os
import mysql.connector


class ModelSale():
    @classmethod
    def get_connection(self):
        return mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['database']
        )
    @classmethod
    def register_sale(self, sale_object):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO SALES (sale_date, total_price, id_user) VALUES (%s, %s, %s)', (
                sale_object.sale_date, sale_object.total_price, sale_object.id_user))
            connection.commit()
            sale_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return sale_id
        except Exception as e:
            print(e)
    @classmethod
    def insert_into_sale_product(self, products, sale_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            sql_statement = 'INSERT INTO PRODUCTS_SALES (id_sale, id_product) VALUES'
            for product in products:
            # concat to sql_statement the values to insert
                sql_statement += ' (' + str(sale_id) + ', ' + str(product['id']) + '),'
            # remove the last comma
            sql_statement = sql_statement[:-1]
            # add the semicolon
            sql_statement += ';'
            # execute the sql statement    
            cursor.execute(sql_statement)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
    @classmethod
    def update_product_stock(self, products):
        try:
            print("updating...")
            print(products)
            connection = self.get_connection()
            cursor = connection.cursor()
            for product in products:
                print(product['product_id'])
                cursor.execute('UPDATE PRODUCTS SET stock = stock - 1 WHERE product_id = %s;', (int(product['product_id']),))
                connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)