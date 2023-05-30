import os
import mysql.connector

class DatabaseConnection():
    def get_conenction():
        return mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            password=os.environ['PASSWORD'],
            database=os.environ['database']
        )
    def destroy_conection(connection, cursor):
        cursor.close()
        connection.close()
        print("Connection closed")