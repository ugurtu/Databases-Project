import re

import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

# Use Total.csv
stvk_u = pd.read_csv("Total.csv", index_col=False, delimiter=',')
names = stvk_u["Strasse"]

#  give ur username, password from EDIs Server
try:
    conn = msql.connect(host='', database="Project", user='root',
                        password='')
    if conn.is_connected():
        i = 1
        cursor = conn.cursor()
        # Out Project
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        for row in stvk_u["Strasse"]:
            # since we have a blank space in Strasse clear it.
            row = row.replace(' ', '')

            # Print the number of row.
            print(i)

            # cursor.execute("INSERT INTO Strassenverkehrsunfälle(Strasse) VALUES (%s)",(row,))
            query_number = str(i)

            # +query_number
            cursor.execute("UPDATE Strassenverkehrsunfälle SET Strassenname = %s WHERE id =" + query_number, (row,))
            i += 1
            conn.commit()

except Error as e:
    print(e)

finally:
    conn.close()
    print("Close Connection")
