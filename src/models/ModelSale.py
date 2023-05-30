from models.DatabaseConnection import DatabaseConnection

class ModelSale(DatabaseConnection):
    @classmethod
    def register_sale(self, sale_object):
        try:
            connection = super().get_conenction()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO SALES (sale_date, total_price, id_user) VALUES (%s, %s, %s)', (
                sale_object.sale_date, sale_object.total_price, sale_object.id_user))
            connection.commit()
            sale_id = cursor.lastrowid
            super().destroy_conection(connection, cursor)
            return sale_id
        except Exception as e:
            print(e)
    @classmethod
    def insert_into_sale_product(self, products, sale_id):
        try:
            connection = super().get_conenction()
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
            super().destroy_conection(connection, cursor)
        except Exception as e:
            print(e)
    @classmethod
    def update_product_stock(self, products):
        try:
            print("updating...")
            print(products)
            connection = super().get_conenction()
            cursor = connection.cursor()
            for product in products:
                print(product['product_id'])
                cursor.execute('UPDATE PRODUCTS SET stock = stock - 1 WHERE product_id = %s;', (int(product['product_id']),))
                connection.commit()
            super().destroy_conection(connection, cursor)
        except Exception as e:
            print(e)