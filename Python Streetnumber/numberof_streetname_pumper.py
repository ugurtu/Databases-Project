import re

import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

# check if everything is working
stvk_u = pd.read_csv("Gelöschte_Hausnummern_korrekt.csv", index_col=False, delimiter=',')
names = stvk_u["Strasse"]

#  give ur username, password from EDIs Server
try:
    conn = msql.connect(host='traktor.internet-box.ch', database="Project", user='root',
                        password='')
    if conn.is_connected():
        i = 1
        counter = 1
        cursor = conn.cursor()

        # Project
        cursor.execute("SELECT DATABASE();")

        # Record is Project.
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Itterate over gelöschte_hausnummern_korrekt.csv
        # as a dataframe.

        for i in stvk_u["Art"]:
            i = i.replace(' ', '')
            print(counter)
            # cursor.execute("INSERT INTO Strassenverkehrsunfälle(Strassenname) VALUES (%s)",(row,))
            query_number = str(counter)

            # +query_number
            if re.match("^[0-9]+$", i):
                cursor.execute("UPDATE Strassenverkehrsunfälle SET Hausnummer = %s WHERE id =" + query_number,
                               (int(i),))
                # Real time changes. In the loop.
                conn.commit()
            counter += 1

        # the connection is

except Error as e:
    print(e)

finally:
    conn.close()
    print("Close Connection")
