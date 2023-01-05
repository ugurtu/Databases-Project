import time

from geopy.geocoders import Nominatim
import pandas as pd
import re

# Make new geolocator object
geolocator = Nominatim(user_agent="coordinateconverter")

# All coordinates which are extracted in the AllCoordinates.csv
# taken by the file in Datas/100120.csv via pandas
coord = pd.read_csv("AllCoordinates.csv")

new_address = pd.DataFrame()
f = open("Coordinates.csv", "a")


def convert2StreetName():
    """
    This method converts the coordinates
    from coord in to a street name.
    Then writes into Coordinates.csv
    :return: None
    """
    for s in coord:
        # Must be 1 because otherwise too much requests
        time.sleep(1)
        a = geolocator.reverse(s)
        string = a.address + "\n"
        # Write to file
        f.write(string)
    f.close()
    cleanup_Street_name()


# From this point on the cleaning up begins.

# read the csv in
d = pd.read_csv("Coordinates.csv", delimiter=',', names=['Art', 'Strasse', 'Ort', '3', '4', '5', '6', '7', '8'])

# make new column with Art/Strasse and Ort the numbers are those in which we are not interested in
d = pd.DataFrame(d, columns=['Art', 'Strasse', 'Ort', '3', '4', '5', '6', '7', '8'])
new_df = d

def cleanup_Street_name():
    # This method replaces all numbers in the column street names.
    # Problem: isdigit() or isnumeric() methods do not work.
    # So use regex.

    counter = 0
    for i in new_df["Strasse"]:
        c = i.lower()
        # counter for letters
        number = len(re.findall('[abcdefghijklmnopqrstuvwxyzäöü]', c))

        # if 0 letters then take from column "Ort" in Coordinates.csv
        if number == 0:
            new_df.iloc[counter]["Strasse"] = new_df.iloc[counter]["Ort"]

        # if A2-A3  in then take Art. Because it is more specific than Ort
        if "A2-A3" in i:
            new_df.iloc[counter]["Strasse"] = new_df.iloc[counter]["Art"]

        # Go to next row needed for new_df.iloc[][] method
        counter += 1
    cleanup_Street_name_A2orA3()


def cleanup_Street_name_A2orA3():
    counter2 = 0
    # itterate over all rows just from strasse.
    for i in new_df["Strasse"]:

        # if it is A2 or A3 only then take again from column of Art
        if ("A2" in i) or ("A3" in i):
            new_df.iloc[counter2]["Strasse"] = new_df.iloc[counter2]["Art"]

        # Go to next row needed for iloc
        counter2 += 1
    last_clean_up_of_numbers()


def last_clean_up_of_numbers():
    """
    This is the last Cleanup of the column street name
    in the dataframe This takes from the Ort the specific Value
    Since it is preciser.
    :return: None.
    """
    counter3 = 0

    for i in new_df["Strasse"]:
        c = i.lower()
        number = len(re.findall('[abcdefghijklmnopqrstuvwxyzäöü]', c))

        if number == 0:
            new_df.iloc[counter3]["Strasse"] = new_df.iloc[counter3]["Ort"]
        counter3 += 1

    """
    This is just for debugging reasons. 
    If we all went correctly. This should print nothing.
    for i in new_df["Strasse"]:
        c = i.lower()
        number = len(re.findall('[abcdefghijklmnopqrstuvwxyzäöü]', c))
    
        if number == 0:
            print(i)
    """
    clean_up_basel()


def clean_up_basel():
    """
    This procedure gives us all the Values which are:
    " Basel". Since we have a blank space this must be a len of 6.
    We want to replace Basel because it is unspecific.
    We want to have an exact location. This is specified in Art column.
    :return: None
    """
    counter4 = 0

    # Iterate over column strasse in new_df
    for i in new_df["Strasse"]:

        # If Basel is in @i present and the len is 6
        # Then take the column of Art because
        # we checked it and the Art column is preciser than Ort
        #
        if "Basel" in i and len(i) == 6:
            new_df.iloc[counter4]["Strasse"] = new_df.iloc[counter4]["Art"]

        counter4 += 1
    """
    This is just for debugging reason.
    To check if everything was correctly.
    If it is correct it should print zero Times Fail.
    
    for i in new_df["Strasse"]:
        c = i.lower()
        number = len(re.findall('[abcdefghijklmnopqrstuvwxyzäöü]', c))

        if number == 0:
            print("FAIL")
    """
    export_new_df_to_csv()


def export_new_df_to_csv():
    new_df.to_csv("Total.csv")
