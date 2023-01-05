import geopandas as gpd
from Connector import Connector
import pandas as pd

"""
This class is just here for query's.
Decided to make this separately for a better overview
"""


# TODO comment query out
def race_cond_30() -> pd.DataFrame:
    """
    Raser Tatbestand 30.
    :return: "Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Speed", "Amount" as pd.Dataframe
    """
    query_string = ("select q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint,m.Speed, count(*) "
                    "as Anzahl from Integrated.Measurements as m,Integrated.Events as "
                    "e, Integrated.Locations as l,Integrated.Quartier as q where m.event_id = "
                    "e.event_id and e.location_id = l.location_id "
                    "and l.Street = q.Strassenname and "
                    "m.Speed > 70 and m.Zone = 30 "
                    "group by q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint,m.Speed;")
    query_connector = Connector()
    zone = query_connector.execute(query_string)

    df = pd.DataFrame(zone, columns=["Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Speed", "Amount"])
    return df


# TODO comment query out
def race_cond_50() -> pd.DataFrame:
    """
    Raser Tatbestand 50.
    :return: "Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Speed", "Amount" as pd.Dataframe
    """

    query_string = ("select q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint,m.Speed, count(*) "
                    "as Anzahl from Integrated.Measurements as m,Integrated.Events as "
                    "e,Integrated.Locations as l,Integrated.Quartier as q where m.event_id = "
                    "e.event_id and e.location_id = l.location_id "
                    "and l.Street = q.Strassenname and "
                    "m.Speed > 100 and m.Zone = 50 "
                    "group by q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint,m.Speed;")
    query_connector = Connector()
    zone = query_connector.execute(query_string)

    df = pd.DataFrame(zone, columns=["Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Speed", "Amount"])
    return df


# TODO comment query out
def speedPercentage() -> pd.DataFrame:
    """
    Average speed in District.

    :return: "Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Average_District" as dataframe
    """
    query_string = ("select q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint, avg(m.Speed) as Durchschnitt "
                    "from Integrated.Measurements as m,Integrated.Events as e,"
                    "Integrated.Locations as l,Integrated.Quartier as q "
                    "where m.event_id = e.event_id "
                    "and e.location_id = l.location_id and l.Street = q.Strassenname "
                    "group by q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint;")
    query_connector = Connector()
    zone = query_connector.execute(query_string)

    df = pd.DataFrame(zone, columns=["Wohnviertel", "StreetName", "HouseNumber", "GeoPoint", "Average_District"])
    return df


# TODO comment query out
def speedQuery_30(speed: int, zone: int) -> pd.DataFrame:
    """
    Exceeding over 30 as amount in one specific street.
    :return: "District", "StreetName", "HouseNumber", "GeoPoint", "Amount" as pd.Dataframe
    """

    query_string = ("select q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint, count(*) "
                    "as Anzahl from Integrated.Measurements as m,Integrated.Events as "
                    "e,Integrated.Locations as l,Integrated.Quartier as q where m.event_id = "
                    "e.event_id and e.location_id = l.location_id and l.Street = q.Strassenname and "
                    "m.Speed > %s and m.Zone = %s "
                    "group by q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint")
    query_connector = Connector()
    zone = query_connector.execute(query_string, (speed, zone))

    df = pd.DataFrame(zone, columns=["District", "StreetName", "HouseNumber", "GeoPoint", "Amount"])
    return df


def speedQuery_50(speed: int, zone: int) -> pd.DataFrame:
    """
    Exceeding over 50 as amount in one specific street.
    :return: "District", "StreetName", "HouseNumber", "GeoPoint", "Zone", "Speed", "Amount" as pd.Dataframe
    """

    query_string = ("select q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint, m.Zone,m.Speed, count(*) "
                    "as Anzahl from Integrated.Measurements as m,Integrated.Events as "
                    "e,Integrated.Locations as l,Integrated.Quartier as q where m.event_id = "
                    "e.event_id and e.location_id = l.location_id "
                    " and l.Street = q.Strassenname and "
                    " m.Speed > %s and m.Zone = %s "
                    "group by q.Wohnviertel, l.Street, l.HouseNumber, l.Geopoint,m.Zone,m.Speed; ")

    query_connector = Connector()
    zone = query_connector.execute(query_string, (speed, zone))

    df = pd.DataFrame(zone, columns=["District", "StreetName", "HouseNumber", "GeoPoint", "Zone", "Speed", "Amount"])
    return df


def getGeoJsonDistrict() -> gpd.GeoDataFrame:
    """
    For map.
    :return: geopandas
    """
    # Read the GeoJson file in for Districts
    geo_json_wo = gpd.read_file("GeoJson/100042.geojson")

    # Rename the colum name
    geo_json_wo.rename(columns={"wov_name": "Wohnviertel"}, inplace=True)

    return geo_json_wo


def getGeoJsonStreetName() -> gpd.GeoDataFrame:
    """
    For map.
    :return: geopandas
    """

    # Read the GeoJson file in for Streetnames
    street = gpd.read_file("GeoJson/100189.geojson")

    # Rename the colum name
    street.rename(columns={'strname': 'Strasse'}, inplace=True)

    return street


def AmountOfStreetInDistrict() -> list:
    """
    Query for number of streets in district.
    :return: list
    """
    # Query string for get all Wohnviertel and Strassenname
    query_string = "SELECT Strassenname, Wohnviertel FROM Quartier"

    # Connector class
    query_connector = Connector()
    districts_and_streets = query_connector.execute(query_string)

    return districts_and_streets


def accident_Pedestrian() -> list:
    """
    Query for pedestrian accidents in district.
    :return: list
    """
    query_string = ("select Street, Wohnviertel, pedestrian, description from Integrated.Accidents as a,"
                    "Integrated.Events as e,Integrated.Locations as l,Integrated.Quartier as q "
                    "where pedestrian = 1 and a.event_id = e.event_id and l.location_id = e.location_id and q.Strassenname = l.Street;")

    # Connector class
    query_connector = Connector()
    pedestrian = query_connector.execute(query_string)

    return pedestrian


def accident_Bicycle() -> list:
    """
    Query for bicycle accidents in district.
    :return: list
    """
    query_string = ("select Street, Wohnviertel, bicycle, description from Integrated.Accidents as a,"
                    "Integrated.Events as e,Integrated.Locations as l,Integrated.Quartier as q "
                    "where bicycle = 1 and a.event_id = e.event_id and l.location_id = e.location_id and q.Strassenname = l.Street;")

    # Connector class
    query_connector = Connector()
    bicycle = query_connector.execute(query_string)

    return bicycle


def accident_motorcycle() -> list:
    """
    Query for motorcycle accidents in district.
    :return: list
    """
    # query for pedestrians
    query_string = ("""select Street, Wohnviertel, motorcycle, description from Integrated.Accidents as a,
                    Integrated.Events as e,Integrated.Locations as l,Integrated.Quartier as q 
                    where motorcycle = 1 and a.event_id = e.event_id 
                    and l.location_id = e.location_id and q.Strassenname = l.Street;""")

    # Connector class
    query_connector = Connector()
    motorcycle = query_connector.execute(query_string)

    return motorcycle


def car_accidents() -> list:
    """
    Query for car accidents in district.
    :return: list
    """
    query_string = (""" select Street, Wohnviertel, description
                      from Integrated.Accidents as a,Integrated.Events as e,Integrated.Locations as l,Integrated.Quartier as q 
                      where bicycle = 0 and motorcycle = 0 and pedestrian = 0
                      and a.event_id = e.event_id
                      and l.location_id = e.location_id
                      and q.Strassenname = l.Street; """)
    query_connector = Connector()
    cars = query_connector.execute(query_string)

    return cars


def hotspot() -> pd.DataFrame:
    """
    Query for Hotspot.
    If violation of:
    55,35,25,65,85
    :return: GeoPoint", "StreetName", "Amount" DataFrame
    """
    query_string = (""" select l.Geopoint,l.Street, count(*) as Amount
from Integrated.Measurements as m,
     Integrated.Events as e,
     Integrated.Locations as l
where ((Zone = 50 and Speed > 55)
    or (Zone = 30 and Speed > 35)
    or (Zone = 20 and Speed > 25)
    or (Zone = 60 and Speed > 65)
    or (Zone = 80 and Speed > 85))
  and m.event_id = e.event_id
  and e.location_id = l.location_id
group by Geopoint,Street;""")
    query_connector = Connector()
    hotspot_query = query_connector.execute(query_string)

    hotspot_vio = pd.DataFrame(hotspot_query, columns=["GeoPoint", "StreetName", "Amount"])
    return hotspot_vio


def all_accidents_exact() -> pd.DataFrame():
    """
    Query for accidents with the geo point.

    IMPORTANT: SELF ACCIDENTS ARE NOT INCLUDED.
    JUST:
     - PEDESTRIAN
     - MOTORCYCLE
     - BICYCLE
    :return: "Category", "pedestrian", "bicycle", "motorcycle", "street", "description",
                                          "GeoPoint", "StreetName", "HouseNumber", "Wohnviertel"
    """

    query = """
   SELECT category,pedestrian, bicycle, motorcycle,street_type,description,geopoint,Street,housenumber,Wohnviertel
    FROM Integrated.Accidents as a, Integrated.Locations as l, Integrated.Events as e,Integrated.Quartier as q
    WHERE a.event_id = e.event_id AND l.location_id = e.location_id AND q.Strassenname = l.Street
    """

    connector = Connector()
    all_accidents = connector.execute(query)

    all_accidents = pd.DataFrame(all_accidents,
                                 columns=["Category", "pedestrian", "bicycle", "motorcycle", "street", "description",
                                          "GeoPoint", "StreetName", "HouseNumber", "Wohnviertel"])

    return all_accidents


def exactTime():
    """
    This query is needed for the analysis document.

    :return: date, hour, street and house number of the accident.
    """
    query = """
    select e.date, b.hour, l.Street, l.HouseNumber
    FROM Integrated.Events as e,
     Integrated.Locations as l,
     Integrated.Accidents as b
    WHERE e.location_id = l.location_id
      and e.event_id = b.event_id
      and (l.Street = "Reinacherstrasse" and l.HouseNumber = 4)
      and (b.bicycle = 1 or (b.bicycle = 1 and b.motorcycle = 1));
        """
