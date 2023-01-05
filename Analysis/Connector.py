import mysql.connector as mysql
from mysql.connector import Error


class Connector:
    """
    This class is a connector class which is needed
    for the connection to our Integrated Databases.

    """

    def __init__(self):
        self.host = ""

    def execute(self, query, *params):
        connection = object
        cursor = object

        try:
            connection = mysql.connect(host='', database="",
                                       user='root', password='')
            print("You are connected")
            cursor = connection.cursor()
            cursor.execute(query, *params)
            records = cursor.fetchall()

            return records

        except Error as e:
            print(e)

        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
