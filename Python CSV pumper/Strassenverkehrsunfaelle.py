import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

# check if everything is working
stvk_u = pd.read_csv("/home/ugur/Desktop/FS22/Databases/group-11/Datas/100120.csv", index_col=False, delimiter=';')

# necessary to clean it up else problems if they are not null
stvk_u = stvk_u.where((pd.notnull(stvk_u)), 0)

#  give ur username, password from EDIs Server
try:
    conn = msql.connect(host='', database="", user='root',
                        password='')
    if conn.is_connected():
        cursor = conn.cursor()
        # Out Project
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS Straassenverkehrsunfälle;')
        print('Creating table....')

        # in the below line please pass the created table statement which you want #to create
        cursor.execute(
            "CREATE TABLE Strassenverkehrsunfälle("
            "`Geo Point` TEXT ,"
            "`Geo Shape` TEXT ,"
            "`Eindeutiger Identifikator des Unfalls` TEXT,"
            "`Beschreibung zum Unfalltyp` TEXT,"
            "`Beschreibung zum Unfalltyp (fr)` TEXT,"
            "`Beschreibung zum Unfalltyp (en)` TEXT,"
            "`Beschreibung der Unfallschwerekategorie` TEXT,"
            "`Beschreibung der Unfallschwerekategorie (fr)` TEXT,"
            "`Beschreibung der Unfallschwerekategorie (en)` TEXT,"
            "`Unfall mit Fussgängerbeteiligung` TEXT,"
            "`Unfall mit Fahrradbeteiligung` TEXT,"
            "`Unfall mit Motorradbeteiligung` TEXT,"
            "`Beschreibung der Strassenart` TEXT,"
            "`Beschreibung der Strassenart (fr)` TEXT,"
            "`Beschreibung der Strassenart (en)` TEXT,"
            "`Unfallort Ost-Koordinaten` INT,"
            "`Unfallort Nord-Koordinaten` INT,"
            " Kanton TEXT,"
            " Gemeindenummer INT,"
            " Unfalljahr INT,"
            " Unfallmonat INT,"
            "`Unfallmonat.1` TEXT,"
            "`Unfallmonat (fr)` TEXT,"
            "`Unfallmonat (en)` TEXT,"
            " Wochentag TEXT,"
            "`Wochentag (fr)` TEXT,"
            "`Wochentag (en)` TEXT,"
            " Unfallstunde TEXT,"
            " Unfalldatum TEXT,"
            " Unfalltyp TEXT,"
            " Unfallschwerekategorie TEXT,"
            " Strassenart TEXT,"
            "`Code des Wochentags` TEXT,"
            "`Unfallstunde.1` INT)")

        print("Table is created....")
        # loop through the data frame
        for i, row in stvk_u.iterrows():
            # here %S means placeholders for attributes of entity
            sql = "INSERT INTO Project.Strassenverkehrsunfälle VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                  "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
