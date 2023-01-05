import pandas as pd
import re

df = pd.read_csv("Coordinates.csv", delimiter=',', names=['Art', 'Strasse', 'Ort', '3', '4', '5', '6', '7', '8'])


def clean_up(df):
    """
    Since we want to also have the deleted Numbers we must extract them in to a new CSV
    Such that we provide a dataloss of 0 for the numbers.

    Because for us, it is not relevant if Bethesda spital is present or not.
    For us, it is important what number Bethesda spital has as an example.

    This script, saves all the numbers in the column Strasse
    before we clean them up in to the Column Art.

    :param df: Dataframe of coordinates.csv
    :return: None
    """
    numbers_with_number = df["Strasse"]
    counter = 0

    for s in numbers_with_number:
        c = s.lower()
        number = len(re.findall('[abcdefghijklmnopqrstuvwxyzäöü]', c))

        if number == 0:
            df.iloc[counter]["Strasse"] = int(s)

        counter += 1

    get_numbers_only(df)


def get_numbers_only(df):
    numbers = df["Strasse"]
    counter = 0

    for i in numbers:
        if isinstance(i, int):
            print(i)
            df.iloc[counter]["Art"] = i
        counter += 1

    df.to_csv("Gelöschte_Hausnummern_korrekt.csv")


if __name__ == "__main__":
    clean_up(df)
