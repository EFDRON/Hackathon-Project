import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

App_title="Disability Report"
App_subtitle="Source: Ministry Of Community Development"



def display_map(df):
    map=folium.Map(location=(24.3,53.8458),
                   zoom_start=7.4,
                   scrollWheelZoom=False,
                    tiles = "CartoDB Positron",
                   )


    choropleth=folium.Choropleth(geo_data="data/ae.json",
                                 data=df,
                                 key_on="feature.properties.name",
                                 columns=("State Name","Count of Emirate"),
                                 highlight=True,
                                 line_opacity=0.8
                                )
    choropleth.geojson.add_to(map)
    for feature in choropleth.geojson.data["features"]:
        feature["properties"]['population']="1233"

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(["name","population"],labels=False)
    )
    st_map=st_folium(map,width=700,height=450)


def main():
    st.set_page_config("GEOSPATIAL DATA")
    st.title(App_title)
    st.caption(App_subtitle)

    #Loading and Modifying the Data
    my_df=pd.read_excel("data/my_analysis.xlsx")
    df = pd.read_excel("data/secret file.xlsx")
    df.rename(columns={"Emirate2": "Emirate"}, inplace=True)
    year=2022
    nationality="Sudan"
    emirates=""
    disability_type="Autism"
    Gender="Male"

    df=df[(df["year"]==year)&
          (df["Nationality"]==nationality) &
          (df["DisabilityCategory2"]==disability_type)&
          (df["Gender"]==Gender)]
    if emirates:
        df=df[(df["Emirate"]==emirates)]
    total=len(df)


    st.write(total)

    st.write(df.head())
    st.write(df.columns)
    #Display Filters And Map
    df_byemirates = pd.read_csv("data/emirates.csv")
    display_map(df_byemirates)
    df_nationality = pd.read_csv("data/nationalities.csv")

    #Display Metrics







main()