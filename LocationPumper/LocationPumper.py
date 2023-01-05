import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import re
import mysql.connector as msql
from mysql.connector import Error

from Analysis.Connector import Connector

# Global object of Connector
a = Connector()

# Global object of Geopy
geolocator = Nominatim(user_agent="coordinateconverter")


def point_getter():
    street_and_house_num = a.execute(
        "SELECT Integrated.Locations.Street,Integrated.Locations.HouseNumber FROM Locations")

    geo_location = pd.DataFrame(columns=["Strasse"])
    # print(street_and_house_num)
    df = pd.DataFrame(street_and_house_num, columns=["Street", "Number"])
    df = df.fillna("")

    d_list = []
    for s, row in df.iloc.iterrows():
        d = str(row["Number"])
        cleaned = re.sub('\D', "", d)
        # print(cleaned)

        if len(cleaned) > 6:
            # print(cleaned)
            cleaned = ""
        cleaned_address = row["Street"] + ", " + str(cleaned)

        if len(str(cleaned)) == 6:
            cleaned = str(cleaned)[:3]
        cleaned_address = row["Street"] + ", " + str(cleaned)

        if len(str(cleaned)) == 4:
            cleaned = str(cleaned)[:2]
        cleaned_address = row["Street"] + ", " + str(cleaned)

        if "Autobahn A2" == row["Street"] or "Autobahn A3" == row["Street"]:
            cleaned_address = row["Street"]

        print(cleaned_address)
        location = do_geocode(cleaned_address + "," + "Basel")
        if location == None:
            pass
        else:
            string = str(location.latitude) + ", " + str(location.longitude)
        # print(location.latitude)+", "+ str(location.longitude)
        d_list.append(string)

        geo_location = pd.DataFrame(d_list)
        geo_location.to_csv("Coordinates.csv")


def do_geocode(address, attempt=1, max_attempts=5):
    try:
        time.sleep(1)
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt + 1)
        raise

    # print(location.longitude, location.latitude)
    # print raw data


def coord_to_Database():
    # Use Total.csv
    coord = pd.read_csv("Coordinates.csv", index_col=False, delimiter=',')

    #  give ur username, password from EDIs Server
    try:
        conn = msql.connect(host='', database="", user='root',
                            password='')
        if conn.is_connected():
            i = 1
            cursor = conn.cursor()
            # Out Project
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            for row in coord["Coord"]:
                # since we have a blank space in Strasse clear it.
                # Print the number of row.

                print(i)

                # cursor.execute("INSERT INTO Strassenverkehrsunfälle(Strasse) VALUES (%s)",(row,))
                query_number = str(i)

                # +query_number
                cursor.execute("UPDATE Locations SET Geopoint = %s WHERE location_id =" + query_number,
                               (row,))
                i += 1
                conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()
        print("Close Connection")


if __name__ == "__main__":
    # point_getter()
    coord_to_Database()


