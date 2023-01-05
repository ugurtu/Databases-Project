# Import Libraries
import branca.colormap as cm
from Connector import Connector
import webbrowser
import pandas as pd
import geopandas as gpd
from pandas_geojson import to_geojson
import numpy as np
import folium
from folium import plugins
import time
import datetime


def slider_time():
    #https://github.com/python-visualization/folium/blob/v0.2.0/folium/utilities.py#L104
    """
    This
    :return:
    """
    lang = 47.5606
    lat = 7.5906
    # tiles = "Stamen Toner"
    tiles = "cartodbpositron"
    zoom_start = 10
    fg = folium.FeatureGroup(name='Speedviolation over 30', show=False)
    global map
    map = folium.Map(location=[lang, lat], tiles=tiles, zoom_start=zoom_start)
    global marker_cluster
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    """
    Grouping Time Slider for cases over 30
    """
    fg = folium.FeatureGroup(name='Timeslider', show=False)

    # dataframe for wohnviertel
    wohnviertel = gpd.read_file("GeoJson/100042.geojson")
    print(wohnviertel)
    query_30_time_slider_connector = Connector()
    query = (
        "SELECT date, Wohnviertel FROM Integrated.Measurements,Integrated.Locations,Integrated.Events,Integrated.Quartier WHERE Zone = %s AND Speed > %s "
        "AND Integrated.Locations.Street = Integrated.Quartier.Strassenname LIMIT 30000")

    time_slider_df = query_30_time_slider_connector.execute(query, (30, 30))
    time_slider_df = pd.DataFrame(time_slider_df, columns=["date", "wov_name"])
    just_cases = time_slider_df.groupby(["date", "wov_name"])['date'].size().reset_index(name='cases')
    just_cases_df = pd.DataFrame(just_cases)

    """
    Get the geometry from Json
    """

    for i, row in wohnviertel.iterrows():
        for j, row2 in just_cases_df.iterrows():
            if row["wov_name"] == row2["wov_name"]:
                just_cases_df["geometry"] = str(row["geometry"])

    """
    Necessary to convert it to geo dataframe
    """
    just_cases_df['date'] = pd.to_datetime(just_cases_df['date'], format="%Y-%m").astype(str)
    max_colour = max(just_cases_df['cases'])
    min_colour = min(just_cases_df['cases'])
    cmap = cm.linear.YlOrRd_09.scale(min_colour, max_colour)
    just_cases_df['color'] = just_cases['cases'].map(cmap)

    wov = just_cases_df['wov_name'].unique().tolist()
    wov_idx = range(len(wov))
    #print(just_cases_df["date"])
    style_dict = {}
    for i in wov_idx:
        wov_loop = wov[i]
        result = just_cases_df[just_cases_df['wov_name'] == wov_loop]
        inner_dict = {}
        for _, r in result.iterrows():
            inner_dict[r['date']] = {'color': r['color'], 'opacity': 0.4}
        style_dict[str(i)] = inner_dict

    print(style_dict)
    countries_df = just_cases_df[['geometry']]
    countries_gdf = gpd.GeoDataFrame(countries_df)
    countries_gdf = countries_gdf.drop_duplicates().reset_index()
    wohnviertel["date"] = just_cases_df["date"]
    map.add_child(plugins.TimeSliderChoropleth(data=wohnviertel.to_json(),styledict=style_dict,name="Timeslider").add_to(fg))
    #map.add_child(folium.LayerControl(collapsed=False))

    map.save("test.html")
    webbrowser.open("test.html")


if __name__ == '__main__':
    slider_time()
