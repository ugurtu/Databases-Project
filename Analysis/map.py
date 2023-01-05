# Import Libraries
import webbrowser
import pandas as pd
import Analysis.querys as query
import folium
from folium import plugins
from branca.element import MacroElement
from jinja2 import Template

__author__ = " Ugur Turhal, Edi Zeqiri "
__date__ = " 2023. 05. 01 "
__version__ = "0.3"
__email__ = "ugur.turhal@unibas.ch, edi.zeqiri@stud.unibas.ch"
__status__ = "FINISHED"
__license__ = "MIT License"


class BindColormap(MacroElement):

    """Binds a colormap to a given layer.
    Such that we are able to deactivate a layer and the legend if it is NOT active
    Parameters
    ----------
    colormap : branca.colormap.ColorMap
        The colormap to bind.
    """

    def __init__(self, layer, colormap):
        super(BindColormap, self).__init__()
        self.layer = layer
        self.colormap = colormap
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
            {{this._parent.get_name()}}.on('overlayadd', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
            {{this._parent.get_name()}}.on('overlayremove', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
                }});
        {% endmacro %}
        """)  # noqa


def branca_color_map():
    return None


def create_map():
    """
    This function creates the Basic map.
    Lang: of Basel
    Lat: of Basel

    Tiles: is the art of the map

    Marker Cluster: To cluster the Exceedings

    Minimap: To take make a minimap of the Map to find faster the destination

    :return: None
    """


    lang = 47.5606
    lat = 7.5906
    tiles = "cartodbpositron"
    tiles_black = "cartodbdark_matter"
    zoom_start = 13.25

    global folium_map
    folium_map = folium.Map(location=[lang, lat], tiles=None, zoom_start=zoom_start)
    """
    black or white tile
    """
    folium.TileLayer(tiles_black, name="Black map").add_to(folium_map)
    folium.TileLayer(tiles,name="Colored map").add_to(folium_map)

    global marker_cluster

    minimap = folium.plugins.MiniMap(tile_layer='cartodbpositron', zoom_level_offset=-6)
    folium_map.add_child(minimap)
    

def amount_of_violation_in_30():
    """
    This method groups every violation after the Street.
    And shows the amount of exceeding in the specific street.
    Since we do not want cluster 100'000 of point in one Street.
    Is it simpler to take just the StreetName and the Number and count.

    :return:
    """

    # Group
    fg = folium.FeatureGroup(name='Violation of 30 km/h & amount', show=False)
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    # Get the dataframe from the query

    # Exact 30 Zone, where speed greater 30. See query in querys.py

    # TODO Comment later in
    df1 = query.speedQuery_30(30, 30)

    # df1 = pd.read_csv("30er.csv")
    # Iterate through the dataframe
    # Split it by "," Then add the marker (Car Symbol right now) #TODO Change symbol?
    # After that cluster it to the feature group.

    for i, row in df1.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='red', icon='car', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>District: \t</b>{:>20} <br> <br> <b>Streetname & Housenumber: \t</b>{:>10} {:>10} <br> <br>  <b>Amunt of exceedings:</b> {:>10} <br> <br>  <b>Zone:</b> {:>10}".
                      format(row["District"],
                             row["StreetName"],
                             row["HouseNumber"],
                             str(row["Amount"]),
                             str(30))

                      , name=row["StreetName"]).add_to(marker_cluster)
    """
    dataframe_30zone_coord = pd.DataFrame()
    dataframe_30zone_coord["Street name"] = df1["StreetName"]
    dataframe_30zone_coord["House number"] = df1["HouseNumber"]
    dataframe_30zone_coord["Amount"] = df1["Amount"]
    dataframe_30zone_coord = dataframe_30zone_coord.sort_values('Amount')
    dataframe_30zone_coord.to_csv("dataframe_30zone_coord.csv")
    """
    # Add to map such that we can tick on and off
    folium_map.add_child(fg)

    # Search Engine after street name
    # Not necessary but nice to have
    service_search = folium.plugins.Search(
        layer=marker_cluster,
        search_label="name",
        placeholder='Search for street names in 30 zone',
        collapsed=True,
    )

    # Add to map
    folium_map.add_child(service_search)


def choroplethForExceeding30():
    """
    This choropleth is for all exceeding over 30.
    It should directly give an overview
    :return: None
    """

    # get json Wohnviertel
    wohnviertel = query.getGeoJsonDistrict()

    # Query for 50
    df = query.speedQuery_30(30, 30)

    # Rename the column name, because Wohnviertel is need.
    # Otherwise, melting would not be successful
    df.rename(columns={"District": "Wohnviertel"}, inplace=True)

    # Sum of all exceeding measurements.
    df_grouped_counts = df.groupby('Wohnviertel')[['Amount']].sum().reset_index()

    # Merge them wohnviertel with the sum
    result = pd.merge(wohnviertel, df_grouped_counts, on="Wohnviertel")
    result["Percentage"] = round(result['Amount'] / result['Amount'].sum() * 100, 2)
    result["Percentage"] = result["Percentage"].astype(str)+" %"

    """
    # export
    df = pd.DataFrame()
    df["Wohnviertel"] = result["Wohnviertel"]
    df["Amount"] = result["Amount"]
    df["Percentage"] = result["Percentage"]
    df = df.sort_values("Amount")
    df.to_csv("Exceeding30%.csv")
    """

    choropleth_exceeding_30 = folium.Choropleth(
        geo_data=result,
        name="Violations in zone 30 (Choropleth)",
        data=df_grouped_counts,
        columns=["Wohnviertel", "Amount","Percentage"],
        key_on='feature.properties.Wohnviertel',
        fill_color="YlOrRd",
        fill_opacity=0.70,
        line_opacity=.35,
        highlight=True,
        show=False,
        line_color='black',
        legend_name='Amount in total (30 zone)'
    )

    choropleth_exceeding_30.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['Wohnviertel', 'Amount',"Percentage"], labels=True, sticky=True)
    )

    for key in choropleth_exceeding_30._children:
        if key.startswith('color_map'):
            branca_color_map = choropleth_exceeding_30._children[key]
            del (choropleth_exceeding_30._children[key])

    # Add choropleth for accidents as child to the map.
    # We add this to the map as a child.
    folium_map.add_child(choropleth_exceeding_30)
    folium_map.add_child(branca_color_map)
    folium_map.add_child(BindColormap(choropleth_exceeding_30, branca_color_map))


def amount_of_violation_in_50():
    """
    This method groups every violation after the Street.
    And shows the amount of exceeding in the specific street.
    Since we do not want cluster 100'000 of point in one Street.
    Is it simpler to take just the StreetName and the Number and count.

    :return:
    """

    # Group
    fg = folium.FeatureGroup(name='Violation of 50 km/h & amount', show=False)
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    # Get the dataframe from the query

    # Exact 50 Zone, where speed greater 50. See query in query's.py
    df1 = query.speedQuery_50(50, 50)
    # df1 = pd.read_csv("50er.csv")

    # Iterate through the dataframe
    # Split it by "," Then add the marker (Car Symbol right now) #TODO Change symbol?
    # After that cluster it to the feature group.

    for i, row in df1.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='red', icon='car', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>District: \t</b>{:>20} <br> <br> <b>Streetname & Housenumber: \t</b>{} {} <br> <br>  <b>Zone:</b> {} <br> <br>  <b>Speed</b> + {} km/h <br> <br>  <b>Amount:</b> {}".
                      format(row["District"],
                             row["StreetName"],
                             row["HouseNumber"],
                             str(row["Zone"]),
                             str(row["Speed"]),
                             str(row["Amount"]))

                      , street=row["StreetName"]).add_to(marker_cluster)

    # Add to map such that we can tick on and off
    folium_map.add_child(fg)

    """
    dataframe_50zone_coord = pd.DataFrame()
    dataframe_50zone_coord["Street name"] = df1["StreetName"]
    dataframe_50zone_coord["House number"] = df1["HouseNumber"]
    dataframe_50zone_coord["Amount"] = df1["Amount"]
    dataframe_50zone_coord = dataframe_50zone_coord.sort_values('Amount')
    dataframe_50zone_coord.to_csv("dataframe_50zone_coord.csv")
    """

    # Search Engine after street name
    # Not necessary but nice to have
    service_search = folium.plugins.Search(
        layer=marker_cluster,
        search_label="street",
        placeholder='Search for street names in 50 zone',
        collapsed=True,
    )

    # Add to map
    folium_map.add_child(service_search)


def choroplethForExceeding50():
    """
    This choropleth is for all exceeding over 50.
    It should directly give an overview
    :return: None
    """

    # get json Wohnviertel
    wohnviertel = query.getGeoJsonDistrict()

    # Query for 50
    df = query.speedQuery_50(50, 50)

    # Rename the column name, because Wohnviertel is need.
    # Otherwise, melting would not be successful
    df.rename(columns={"District": "Wohnviertel"}, inplace=True)

    # Sum of all exceeding measurements.
    df_grouped_counts = df.groupby('Wohnviertel')[['Amount']].sum().reset_index()

    # Merge them wohnviertel with the sum
    result = pd.merge(wohnviertel, df_grouped_counts, on="Wohnviertel")
    result["Percentage"] = round(result['Amount'] / result['Amount'].sum() * 100, 2)
    result["Percentage"] = result["Percentage"].astype(str) + " %"

    # export
    """
    df = pd.DataFrame()
    df["Wohnviertel"] = result["Wohnviertel"]
    df["Amount"] = result["Amount"]
    df["Percentage"] = result["Percentage"]
    df = df.sort_values("Amount")
    df.to_csv("Exceeding50%.csv")
    """
    choropleth_exceeding_50 = folium.Choropleth(
        geo_data=result,
        name="Violations in zone 50 (Choropleth)",
        data=df_grouped_counts,
        columns=["Wohnviertel", "Amount","Percentage"],
        key_on='feature.properties.Wohnviertel',
        fill_color="YlOrRd",
        fill_opacity=0.70,
        line_opacity=.35,
        highlight=True,
        show=False,
        line_color='black',
        legend_name='Amount in total (50 zone)'
    )

    choropleth_exceeding_50.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['Wohnviertel', 'Amount',"Percentage"], labels=True, sticky=True)
    )

    for key in choropleth_exceeding_50._children:
        if key.startswith('color_map'):
            branca_color_map = choropleth_exceeding_50._children[key]
            del (choropleth_exceeding_50._children[key])

    # Add choropleth for accidents as child to the map.
    # We add this to the map as a child.
    folium_map.add_child(choropleth_exceeding_50)
    folium_map.add_child(branca_color_map)
    folium_map.add_child(BindColormap(choropleth_exceeding_50, branca_color_map))


def race_violation_over40_in_30():
    """
    We want to take this, because.
    Over 40 km/h exceeding in 30 Zone, in Switzerland that is a
    Rasertatbestand. This method shows them all.

    :return: none
    """

    fg = folium.FeatureGroup(name='Speed violation over 40km/h in Zone 30', show=False)
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    df1 = query.race_cond_30()

    for i, row in df1.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='orange', icon='car', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>District: \t</b>{:>20} <br> <br> <b>Streetname & Housenumber: \t</b>{} {} <br> <br>  <b>Speed</b> {} km/h <br> <br>  <b>Amount:</b> {}".
                      format(row["Wohnviertel"],
                             row["StreetName"],
                             row["HouseNumber"],
                             str(row["Speed"]),
                             str(row["Amount"]))).add_to(marker_cluster)
        # popup=
    folium_map.add_child(fg)
    """
    dataframe_30raser = pd.DataFrame()
    dataframe_30raser["Street name"] = df1["StreetName"]
    dataframe_30raser["House number"] = df1["HouseNumber"]
    dataframe_30raser["Speed"] = df1["Speed"]
    dataframe_30raser["Amount"] = df1["Amount"]
    dataframe_30raser = dataframe_30raser.sort_values("Speed")
    dataframe_30raser.to_csv("raser_tatbestand_30.csv")
    """

def race_violation_over50_in_50():
    """
    We want to take this, because.
    Over 50 km/h exceeding in 50 Zone, in Switzerland that is a
    Rasertatbestand. This method shows them all in clusters.

    :return: none
    """

    # We group this group such that we can set a tick,
    # when we want to show the exact points
    fg = folium.FeatureGroup(name='Speed violation over 50km/h in Zone 50', show=False)

    # To cluster the exceeding
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    df1 = query.race_cond_50()

    for i, row in df1.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='orange', icon='car', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>District: \t</b>{:>20} <br> <br> <b>Streetname & Housenumber: \t</b>{} {} <br> <br>  <b>Speed</b> {} km/h <br> <br>  <b>Amount:</b> {}".
                      format(row["Wohnviertel"],
                             row["StreetName"],
                             row["HouseNumber"],
                             str(row["Speed"]),
                             str(row["Amount"]))).add_to(marker_cluster)
        # popup=
    folium_map.add_child(fg)
    """
    dataframe_50raser = pd.DataFrame()
    dataframe_50raser["Street name"] = df1["StreetName"]
    dataframe_50raser["House number"] = df1["HouseNumber"]
    dataframe_50raser["Speed"] = df1["Speed"]
    dataframe_50raser["Amount"] = df1["Amount"]
    dataframe_50raser = dataframe_50raser.sort_values('Speed')
    dataframe_50raser.to_csv("raser_tatbestand_50.csv")
    """

def average_exceeding():
    """
    This method shows the violation of the districts by the mean
    All zones were included. All of them were shown in a choropleth map.

    :return: none
    """

    # Read GeoJson in
    wohnviertel = query.getGeoJsonDistrict()

    # Make here the query for average Speed in District
    # TODO comment in
    avg_speed_df = query.speedPercentage()

    # Then group by Wohnviertel.
    # Then calculate the mean in Wohnviertel
    # IMPORTANT: Use reset index otherwise the column will not be correctly named.
    avg_grouped = avg_speed_df.groupby('Wohnviertel')[['Average_District']].mean().reset_index()

    # Merge with the geoJson file.
    # On the column Wohnviertel
    # Needed for the Choropleth
    merged_with_wov = pd.merge(wohnviertel, avg_grouped, on="Wohnviertel")

    # Here we create the choropleth map.
    # Geo data is still the geojson. From merged_with_wov
    average_speed_choro = folium.Choropleth(
        geo_data=merged_with_wov,
        name="Average mean in zone 30 (Choropleth)",
        data=avg_grouped,
        columns=["Wohnviertel", "Average_District"],
        key_on='feature.properties.Wohnviertel',
        fill_color="YlOrRd",
        fill_opacity=0.70,
        line_opacity=.35,
        highlight=True,
        show=False,
        line_color='black',
        legend_name="General Mean of exceeding in district"
    )

    # This method adds the tooltip to the choropleth map,
    # Such that we can hover over the district and see the name,
    # And the average speed in the district.

    average_speed_choro.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['Wohnviertel', 'Average_District'], labels=True, sticky=True)
    )

    for key in average_speed_choro._children:
        if key.startswith('color_map'):
            branca_color_map = average_speed_choro._children[key]
            del (average_speed_choro._children[key])

    # Add choropleth for accidents as child to the map.
    # We add this to the map as a child.
    folium_map.add_child(average_speed_choro)
    folium_map.add_child(branca_color_map)
    folium_map.add_child(BindColormap(average_speed_choro, branca_color_map))


# TODO Make this as Location of average speeding with exact points. Since we have the coordinates.
def average_exceeding_detail():
    """
      This method shows the violation of the districts by the mean
      All zones were included. All of them were shown with the exact geo point.
      On the map.

      :return: none
      """

    fg = folium.FeatureGroup(name="Average mean speed", show=False)
    # Get the query it is in the querys.py

    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    # TODO Comment in after testing
    average_in_detail = query.speedPercentage()

    # average_in_detail = pd.read_csv("avg.csv")
    for i, row in average_in_detail.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      icon=folium.Icon(color='cadetblue', icon='cab', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>District: \t</b>{:>20} <br> <br> <b>Streetname & Housenumber: \t</b>{} {} <br> <br>  <b>Average Speed:</b> {}".
                      format(row["Wohnviertel"],
                             row["StreetName"],
                             row["HouseNumber"],
                             row["Average_District"])
                      , name=row["StreetName"]).add_to(marker_cluster)
        # popup=

    folium_map.add_child(fg)


def clean_geoJson_017():
    """
    This name renames the colum name in Gemeinde.
    It also Makes a new column with colors, which are
    defined by Hex Values.

    :return: None
    """
    hover_streets(folium_map)
    choropleth_Amount_of_str()


def hover_streets(map):
    """
    This gets the map and adds the invisible hovering. Reached by 'color': '#FF000000',
    First read the 100189.geojson.

    :param map:
    :return: None
    """
    street = query.getGeoJsonStreetName()

    style_function = lambda x: {
        'fillColor': '#FF000000',
        'color': '#FF000000',
        'weight': 20,
        'fill': True,
        'fillOpacity': 0
    }

    fg = folium.FeatureGroup(name='Streetnames', show=True)

    folium.GeoJson(street, overlay=False, tooltip=folium.GeoJsonTooltip(fields=["Strasse"], labels=False, sticky=True),
                   style_function=style_function).add_to(fg)

    map.add_child(fg)


def choropleth_Amount_of_str():
    wohnviertel = query.getGeoJsonDistrict()
    wohnviertel.rename(columns={'Wohnviertel': 'District'}, inplace=True)
    # From query's.py
    districts_and_streets = query.AmountOfStreetInDistrict()

    # Make a Dataframe
    df_sd = pd.DataFrame(districts_and_streets, columns=["Strassenname", "District"])

    # Then group by Wohnviertel and Count.
    # The method .reset_index() is needed for the new column header
    str_name_and_dis = df_sd.groupby(["District"])["Strassenname"].count().reset_index(name="Number of Streets")

    result = pd.merge(wohnviertel, str_name_and_dis, on="District")
    # Choropleth to show the amount of streets in district.
    # wohnviertel is of type choropleth

    choropleth_ds = folium.Choropleth(
        geo_data=result,
        name="Amount of Streets in district (Choropleth)",
        data=str_name_and_dis,
        columns=["District", "Number of Streets"],
        key_on='feature.properties.District',
        fill_color="YlOrRd",
        fill_opacity=0.55,
        line_opacity=.35,
        highlight=True,
        line_color='black',
        legend_name="Amount of Street in District",
        smooth_factor=0.25
    )

    for key in choropleth_ds._children:
        if key.startswith('color_map'):
            branca_color_map = choropleth_ds._children[key]
            del (choropleth_ds._children[key])

    # We add this to the map as a child.
    folium_map.add_child(choropleth_ds)
    folium_map.add_child(branca_color_map)
    folium_map.add_child(BindColormap(choropleth_ds, branca_color_map))
    # And show the tooltip to hover.
    choropleth_ds.geojson.add_child(
        # TODO Implement number of streets not working
        folium.features.GeoJsonTooltip(fields=['District', "Number of Streets"], labels=True, sticky=True)
    )

    # This is needed to show the
    folium.LayerControl(collapsed=False).add_to(folium_map)

    # SAVE HTML
    folium_map.save("map.html")
    webbrowser.open("map.html")


def accidents():
    # from query's.py
    wohnviertel = query.getGeoJsonDistrict()

    # from query's.py
    pedestrian = query.accident_Pedestrian()

    # from query's.py
    bicycle = query.accident_Bicycle()

    # from query's.py
    motorcycle = query.accident_motorcycle()

    # cars accident from query's.py
    cars = query.car_accidents()

    df2_pedmobi_clean = pd.DataFrame()
    # (ped + Bi) or (ped + mo)
    df1 = query.all_accidents_exact()
    df2_pedmobi = df1[
        (df1["pedestrian"] == 1) & (df1["bicycle"] == 1) | (df1["pedestrian"] == 1) & (df1["motorcycle"] == 1)]
    df2_pedmobi_clean["Wohnviertel"] = list(df2_pedmobi["Wohnviertel"])
    df2_pedmobi_clean["pedestrian"] = list(df2_pedmobi["pedestrian"])

    pedmobi_clean = df2_pedmobi_clean.groupby(["Wohnviertel"])["pedestrian"].count().reset_index(
        name="Pedestrian Involved in Accident")

    # (bi) and (mo)
    df2_mobi_clean = pd.DataFrame()
    df1_mobi = query.all_accidents_exact()
    df2_mobi = df1_mobi[(df1["bicycle"] == 1) & (df1_mobi["motorcycle"] == 1)]
    df2_mobi_clean["Wohnviertel"] = list(df2_mobi["Wohnviertel"])
    df2_mobi_clean["bicycle"] = list(df2_mobi["bicycle"])
    mobi_clean = df2_mobi_clean.groupby(["Wohnviertel"])["bicycle"].count().reset_index(
        name="Bicycle Involved in Accident")

    # dataframe pedestrian
    data_frame_p = pd.DataFrame(pedestrian, columns=["StreetName", "Wohnviertel", "Pedestrian", "Description"])

    data_frame_bi = pd.DataFrame(bicycle, columns=["StreetName", "Wohnviertel", "Bicycle", "Description"])

    # dataframe bicycle
    data_frame_mo = pd.DataFrame(motorcycle, columns=["StreetName", "Wohnviertel", "Motorcycle", "Description"])

    data_frame_cars = pd.DataFrame(cars, columns=["StreetName", "Wohnviertel", "Description"])

    data_frame_cars["Cars"] = pd.Series([1 for x in range(len(data_frame_cars.index))])

    car = data_frame_cars.groupby(["Wohnviertel"])["Cars"].count().reset_index(
        name="Cars Involved in Accident")

    # print(car.head())
    # Group pedestrian accidents by Wohnviertel
    ped = data_frame_p.groupby(["Wohnviertel"])["Pedestrian"].count().reset_index(
        name="Pedestrian Involved in Accident")
    ped = pd.concat([ped, pedmobi_clean]).groupby(['Wohnviertel']).sum().reset_index()

    # Group bicycle accidents by Wohnviertel
    bi = data_frame_bi.groupby(["Wohnviertel"])["Bicycle"].count().reset_index(name="Bicycle Involved in Accident")
    bi = pd.concat([bi, mobi_clean]).groupby(['Wohnviertel']).sum().reset_index()
    # Group motorcycle accidents by Wohnviertel
    mo = data_frame_mo.groupby(["Wohnviertel"])["Motorcycle"].count().reset_index(
        name="Motorcycle Involved in Accident")

    # must be here
    mo.loc[len(mo)] = ["Bettingen", 0]

    res = pd.merge(car, ped, on="Wohnviertel")
    res = pd.merge(res, bi, on="Wohnviertel")
    res = pd.merge(res, mo, on="Wohnviertel")

    result = pd.merge(wohnviertel, car, on="Wohnviertel")
    result = pd.merge(result, ped, on="Wohnviertel")
    result = pd.merge(result, bi, on="Wohnviertel")
    result = pd.merge(result, mo, on="Wohnviertel")

    result["Total"] = result["Pedestrian Involved in Accident"] + result["Bicycle Involved in Accident"] + result[
        "Motorcycle Involved in Accident"] + result["Cars Involved in Accident"]
    result["Total"].astype(str)

    """
    #export
    acc_df_dis = pd.DataFrame()
    acc_df_dis["Wohnviertel"] = result["Wohnviertel"]
    acc_df_dis["Total"] = result["Total"]
    acc_df_dis.to_csv("Accidents_District.csv")
    """

    accidents_choropleth = folium.Choropleth(
        geo_data=result,
        name="All Accidents (Choropleth)",
        data=res,
        columns=["Wohnviertel", "Pedestrian Involved in Accident", "Bicycle Involved in Accident",
                 "Motorcycle Involved in Accident", "Cars Involved in Accident", "Total"],
        key_on='feature.properties.Wohnviertel',
        fill_color="OrRd",
        fill_opacity=0.55,
        line_opacity=.35,
        highlight=True,
        show=False,
        line_color='black',
        legend_name='Amount of Accidents in district',
        smooth_factor=0.2
    )

    for key in accidents_choropleth._children:
        if key.startswith('color_map'):
            branca_color_map = accidents_choropleth._children[key]
            del (accidents_choropleth._children[key])

    # And show the tooltip to hover.
    accidents_choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['Wohnviertel', 'Pedestrian Involved in Accident', "Bicycle Involved in Accident",
                    "Motorcycle Involved in Accident", "Cars Involved in Accident", "Total"], labels=True, sticky=True)
    )

    # Add choropleth for accidents as child to the map.
    # We add this to the map as a child.
    folium_map.add_child(accidents_choropleth)
    folium_map.add_child(branca_color_map)
    folium_map.add_child(BindColormap(accidents_choropleth, branca_color_map))


def hotspots():
    hotspot = query.hotspot()

    all_accidents = accidents_hotspot()

    df2 = pd.DataFrame()
    df = hotspot.groupby("StreetName")["Amount"].sum().reset_index()

    filter = df["Amount"] > 11000
    df = df.where(filter)
    df = df.dropna()
    df = df.drop_duplicates()

    df2["StreetName"] = all_accidents["StreetName"]

    result = pd.merge(all_accidents, df, on="StreetName")
    result.rename(columns={'Amount': 'Amount of violations in street'}, inplace=True)
    result.rename(columns={'Total': 'Accidents in total'}, inplace=True)
    #result = result.drop_duplicates()

    """
    to_csv = pd.DataFrame()
    to_csv["StreetName"] = result["StreetName"]
    to_csv["Amount of violations in street"] = result["Amount of violations in street"]
    to_csv["Pedestrian Involved in Accident"] = result["Pedestrian Involved in Accident"]
    to_csv["Bicycle Involved in Accident"] = result["Bicycle Involved in Accident"]
    to_csv["Motorcycle Involved in Accident"] = result["Motorcycle Involved in Accident"]
    to_csv["Accidents in total"] = result["Accidents in total"]
    to_csv.to_csv("Hotspot.csv")
    """

    print(result.head(10))
    fg = folium.FeatureGroup(name='Hotspot', show=False)

    style_function = lambda x: {
        'fillColor': 'Orange',
        'show': False,
        'color': 'grey',
        'weight': 2.5,
        'fill': True,
        'fillOpacity': 0.55,
        'lineOpacity': 0.55
    }

    folium.GeoJson(result, overlay=False, tooltip=folium.GeoJsonTooltip(
        fields=["StreetName", "Amount of violations in street", "Pedestrian Involved in Accident", "Cars Involved in Accident",
                "Bicycle Involved in Accident", "Motorcycle Involved in Accident", "Accidents in total"], labels=True, sticky=True),
                   style_function=style_function).add_to(fg)

    folium_map.add_child(fg)


def accidents_hotspot():
    """
    All the accidents
    :return:
    """
    # from query's.py
    strassenname = query.getGeoJsonStreetName()
    strassenname.rename(columns={'Strasse': 'StreetName'}, inplace=True)
    # print(strassenname.columns)
    # from query's.py
    pedestrian = query.accident_Pedestrian()

    # from query's.py
    bicycle = query.accident_Bicycle()

    # from query's.py
    motorcycle = query.accident_motorcycle()

    # cars accident from query's.py
    cars = query.car_accidents()

    df2_pedmobi_clean = pd.DataFrame()
    # (ped + Bi) or (ped + mo)
    df1 = query.all_accidents_exact()
    df2_pedmobi = df1[
        (df1["pedestrian"] == 1) & (df1["bicycle"] == 1) | (df1["pedestrian"] == 1) & (df1["motorcycle"] == 1)]
    df2_pedmobi_clean["StreetName"] = list(df2_pedmobi["StreetName"])
    df2_pedmobi_clean["pedestrian"] = list(df2_pedmobi["pedestrian"])

    pedmobi_clean = df2_pedmobi_clean.groupby(["StreetName"])["pedestrian"].count().reset_index(
        name="Pedestrian Involved in Accident")

    # (bi) and (mo)
    df2_mobi_clean = pd.DataFrame()
    df1_mobi = query.all_accidents_exact()
    df2_mobi = df1_mobi[(df1["bicycle"] == 1) & (df1_mobi["motorcycle"] == 1)]
    df2_mobi_clean["Wohnviertel"] = list(df2_mobi["Wohnviertel"])
    df2_mobi_clean["bicycle"] = list(df2_mobi["bicycle"])
    mobi_clean = df2_mobi_clean.groupby(["Wohnviertel"])["bicycle"].count().reset_index(
        name="Bicycle Involved in Accident")

    # dataframe pedestrian
    data_frame_p = pd.DataFrame(pedestrian, columns=["StreetName", "Wohnviertel", "Pedestrian", "Description"])
    # for i, row in data_frame_p.iterrows():
    #    if row["Wohnviertel"] == "Bettingen":
    #        print(row["Wohnviertel"])
    # dataframe bicycle
    data_frame_bi = pd.DataFrame(bicycle, columns=["StreetName", "Wohnviertel", "Bicycle", "Description"])

    # dataframe bicycle
    data_frame_mo = pd.DataFrame(motorcycle, columns=["StreetName", "Wohnviertel", "Motorcycle", "Description"])

    data_frame_cars = pd.DataFrame(cars, columns=["StreetName", "Wohnviertel", "Description"])

    data_frame_cars["Cars"] = pd.Series([1 for x in range(len(data_frame_cars.index))])

    car = data_frame_cars.groupby(["StreetName"])["Cars"].count().reset_index(
        name="Cars Involved in Accident")

    # Group pedestrian accidents by Wohnviertel
    ped = data_frame_p.groupby(["StreetName"])["Pedestrian"].count().reset_index(
        name="Pedestrian Involved in Accident")
    ped = pd.concat([ped, pedmobi_clean]).groupby(['StreetName']).sum().reset_index()
    # Group bicycle accidents by Wohnviertel
    bi = data_frame_bi.groupby(["StreetName"])["Bicycle"].count().reset_index(name="Bicycle Involved in Accident")

    bi = pd.concat([bi, mobi_clean]).groupby(['StreetName']).sum().reset_index()
    # Group motorcycle accidents by Wohnviertel
    mo = data_frame_mo.groupby(["StreetName"])["Motorcycle"].count().reset_index(
        name="Motorcycle Involved in Accident")

    # must be here
    mo.loc[len(mo)] = ["Bettingen", 0]

    res = pd.merge(car, ped, on="StreetName")
    res = pd.merge(res, bi, on="StreetName")
    res = pd.merge(res, mo, on="StreetName")

    result = pd.merge(strassenname, car, on="StreetName")
    result = pd.merge(result, ped, on="StreetName")
    result = pd.merge(result, bi, on="StreetName")
    result = pd.merge(result, mo, on="StreetName")

    result["Total"] = result["Pedestrian Involved in Accident"] + result["Bicycle Involved in Accident"] + result[
        "Motorcycle Involved in Accident"] + result["Cars Involved in Accident"]

    # print(result.head())
    result = result.where(result["Total"] > 50)
    return result


def all_accidents_ped():
    # We group this group such that we can set a tick,
    # when we want to show the exact points
    fg = folium.FeatureGroup(name='Accidents involving Pedestrians', show=False)

    # To cluster the exceeding
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    df1 = query.all_accidents_exact()
    df2 = df1[(df1["pedestrian"] == 1) & (df1["bicycle"] == 1) | (df1["pedestrian"] == 1) & (df1["motorcycle"] == 1) | (df1["pedestrian"] == 1)]

    for i, row in df2.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      show=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='blue', icon='female', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>Category \t</b>{:>20} <br> <br> <b>Street type </b>{} <br> <br>  <b>Description</b> {} <br> <br>  <b>Street name House number</b> {} {}".
                      format(row["Category"],
                             row["street"],
                             row["description"],
                             row["StreetName"],
                             str(row["HouseNumber"])
                             )).add_to(marker_cluster)
        # popup=
    """
    folium_map.add_child(fg)
    dataframe_ped_acc = pd.DataFrame()
    dataframe_ped_acc["Street name"] = df2["StreetName"]
    dataframe_ped_acc["House number"] = df2["HouseNumber"]
    dataframe_ped_acc["Ped"] = pd.Series([1 for x in range(len(df2.index))])
    dataframe_ped_acc.to_csv("ped.csv")
    """

def all_accidents_bi():
    # We group this group such that we can set a tick,
    # when we want to show the exact points
    fg = folium.FeatureGroup(name='Accidents involving Bicycle', show=False)

    # To cluster the exceeding
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    df1 = query.all_accidents_exact()
    df2 = df1[(df1["bicycle"] == 1) & (df1["motorcycle"] == 1) | (df1["bicycle"] == 1)]
    # print(df2.head())
    for i, row in df2.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      show=False,
                      # icon=icon_plane,
                      icon=folium.Icon(color='green', icon='bicycle', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>Category \t</b>{:>20} <br> <br> <b>Street type </b>{} <br> <br>  <b>Description</b> {} <br> <br>  <b>Street name House number</b> {} {}".
                      format(row["Category"],
                             row["street"],
                             row["description"],
                             row["StreetName"],
                             str(row["HouseNumber"])
                             )).add_to(marker_cluster)
        # popup=
    folium_map.add_child(fg)
    """
    dataframe_bi_acc = pd.DataFrame()
    dataframe_bi_acc["Street name"] = df2["StreetName"]
    dataframe_bi_acc["House number"] = df2["HouseNumber"]
    dataframe_bi_acc["Ped"] = pd.Series([1 for x in range(len(df2.index))])
    dataframe_bi_acc.to_csv("bicycle.csv")
    """

def all_accidents_big():
    # We group this group such that we can set a tick,
    # when we want to show the exact points
    fg = folium.FeatureGroup(name='Accidents involving all participants', show=False)

    # To cluster the exceeding
    marker_cluster = folium.plugins.MarkerCluster().add_to(fg)

    df1 = query.all_accidents_exact()
    df2 = df1[(df1["pedestrian"] == 1) & (df1["bicycle"] == 1) & (df1["motorcycle"] == 1)]
    # print(df2.head())
    for i, row in df2.iterrows():
        geo1, geo2 = row["GeoPoint"].split(",")
        folium.Marker(location=(geo1, geo2),
                      radius=3,
                      # color='red',
                      fill=False,
                      show=False,
                      icon=folium.Icon(color='red', icon='ambulance', prefix='fa'),
                      fill_opacity=0.6,
                      tooltip="<b>Category \t</b>{:>20} <br> <br> <b>Street type </b>{} <br> <br>  <b>Description</b> {} <br> <br>  <b>Street name House number</b> {} {}".
                      format(row["Category"],
                             row["street"],
                             row["description"],
                             row["StreetName"],
                             str(row["HouseNumber"])
                             )).add_to(marker_cluster)
        # popup=
    folium_map.add_child(fg)


"""
        THIS IS NOT WORKING WITH THE MAP 
        IF NEEDED CREATE NEW HTML AND USE DICTIONARY
        
def slider_time():

    Grouping Time Slider for cases over 30
    

    # dataframe for wohnviertel
    wohnviertel = gpd.read_file("GeoJson/100042.geojson")

    query_30_time_slider_connector = Connector()
    query = (
        "SELECT date, Wohnviertel FROM Integrated.Measurements,Integrated.Locations,Integrated.Events,Integrated.Quartier WHERE Zone < %s AND Speed > %s "
        "AND Integrated.Locations.Street = Integrated.Quartier.Strassenname LIMIT 30000")

    time_slider_df = query_30_time_slider_connector.execute(query, (30, 30))
    time_slider_df = pd.DataFrame(time_slider_df, columns=["date", "wov_name"])
    just_cases = time_slider_df.groupby(["date", "wov_name"])['date'].size().reset_index(name='cases')
    just_cases_df = pd.DataFrame(just_cases)

    sname_and_dis = df_sd.groupby(["Wohnviertel"])["Strassenname"].count().reset_index(name="Counts")


    Get the geometry from Json


    for i, row in wohnviertel.iterrows():
        for j, row2 in just_cases_df.iterrows():
            if row["wov_name"] == row2["wov_name"]:
                just_cases_df["geometry"] = str(row["geometry"])


    Necessary to convert it to geo dataframe

    just_cases_df['date'] = pd.to_datetime(just_cases_df['date'].astype(str), format='%Y.%m')
    print(just_cases_df["date"])
    max_colour = max(just_cases_df['cases'])
    min_colour = min(just_cases_df['cases'])
    cmap = cm.linear.YlOrRd_09.scale(min_colour, max_colour)
    just_cases_df['color'] = just_cases_df['cases'].map(cmap)

    wov = just_cases_df['wov_name'].unique().tolist()
    wov_idx = range(len(wov))
    # print(just_cases_df["date"])
    style_dict = {}
    for i in wov_idx:
        wov_loop = wov[i]
        result = just_cases_df[just_cases_df['wov_name'] == wov_loop]
        inner_dict = {}
        for _, r in result.iterrows():
            inner_dict[r['date']] = {'color': r['color'], 'opacity': 0.4}
        style_dict[str(i)] = inner_dict

    # print(style_dict)
    countries_df = just_cases_df[['geometry']]
    countries_gdf = gpd.GeoDataFrame(countries_df)

    # map.add_child(plugins.TimeSliderChoropleth(data=wohnviertel.to_json(),styledict=style_dict))
    folium_map.add_child(
        plugins.TimeSliderChoropleth(data=wohnviertel.to_json(), styledict=style_dict, name="Timeslider", overlay=True))

    # folium.LayerControl(collapsed=False).add_to(map)
    # a = cmap(c)
    # map.add_child(c)

    # map.save("test.html")
    # webbrowser.open("test.html")
"""

if __name__ == '__main__':
    # p0 = multiprocessing.Process(target=create_map)
    create_map()
    hotspots()
    amount_of_violation_in_30()
    choroplethForExceeding30()
    amount_of_violation_in_50()
    choroplethForExceeding50()
    accidents()
    all_accidents_ped()
    all_accidents_bi()
    all_accidents_big()
    race_violation_over40_in_30()
    race_violation_over50_in_50()
    average_exceeding()
    average_exceeding_detail()
    clean_geoJson_017()
