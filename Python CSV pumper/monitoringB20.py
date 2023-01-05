import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

# check if everything is working
gmb20 = pd.read_csv("/home/ugur/Desktop/FS22/Databases/group-11/Datas/100200.csv", index_col=False, delimiter=';')
print(gmb20.head(5))

#  give ur username, password from EDIs Server

try:
    conn = msql.connect(host='traktor.internet-box.ch', database="Project", user='root',
                        password='')
    if conn.is_connected():
        cursor = conn.cursor()
        # Out Project
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS gm;')
        print('Creating table....')

        # in the below line please pass the created table statement which you want #to create
        cursor.execute(
            "CREATE TABLE gm("
            " Timestamp TEXT,"
            "`Messung ID` INT,"
            "`Richtung ID` INT,"
            "`Geschwindigkeit` DOUBLE,"
            " Zeit TEXT,"
            " Datum TEXT,"
            "`Datum und Zeit` TEXT,"
            " Messbeginn TEXT,"
            " Messende TEXT,"
            " Zone INT,"
            " Ort TEXT,"
            " Richtung TEXT,"
            " Geopunkt TEXT,"
            " Übertretungsquote DOUBLE,"
            " GeschwindigkeitV50 DOUBLE,"
            " GeschwindigkeitV85 DOUBLE,"
            " Strasse TEXT,"
            " Hausnummer TEXT,"
            " Fahrzeuge INT,"
            " Fahrzeuglänge DOUBLE,"
            "`Kennzahalen pro Mess-Standort` TEXT)")

        print("Table is created....")
        # loop through the data frame
        for i, row in gmb20.iterrows():
            # here %S means string values
            sql = "INSERT INTO Project.gm VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                  "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            # Make commit inside, then we have real time entries.
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    conn.close()
    print("Connection closed")

