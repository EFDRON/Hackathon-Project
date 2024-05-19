import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

App_TITLE="Fraud and identity theft report"
APP_SUBTITLE="Source: Federal Trade Comission"



def display_map(df,year,quarter):
    df = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
    map=folium.Map(location=(38,-96.5),
                   zoom_start=4,
                   scrollWheelZoom=False,
                   tiles="cartoDB positron")
    choropleth=folium.Choropleth(geo_data="data/us-state-boundaries.geojson",
                                 data=df,
                                 key_on="feature.properties.name",
                                 columns=("State Name","State Total Reports Quarter"),
                                 line_opacity=0.5,
                                 highlight=True
                                 )
    choropleth.geojson.add_to(map)
    df=df.set_index("State Name")
    state_name="California"
    st.write(df.loc[state_name,"State Pop"][0])
    for feature in choropleth.geojson.data["features"]:
        state_name=feature["properties"]["name"]
        feature["properties"]['population']="Populaion: "+str('{:,}'.format(df.loc[state_name,"State Pop"][0]) if state_name in list(df.index) else "N/A" )
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(["name","population"],labels=False))

    st_map=st_folium(map,width=700,height=450)

    st.write(df.shape)
    st.write(df.head())
    st.write(df.columns)


def display_fraud_facts(df,year,quarter,state_name,report_type,field_name,metric_title,number_format="${:,}",is_median=False):

    df = df[(df["Year"] == year) & (df["Quarter"] == quarter) & (df["Report Type"] == report_type)]
    if state_name:
        df = df[(df["State Name"] == state_name)]

    df.drop_duplicates(inplace=True)
    if is_median:
        total = df[field_name].sum()/len(df) if len(df) else 0
    else:
        total = df[field_name].sum()

    st.metric(metric_title, number_format.format(round(total)))

def main():

    st.set_page_config(App_TITLE)
    st.title(App_TITLE)
    st.caption(APP_SUBTITLE)
    year = 2022
    quarter = 1
    state_name = ""
    report_type = "Fraud"
    metric_title = f"Total number of {report_type} reports"
    #Load Data
    #df_continental=pd.read_csv("data/AxS-Continental_Full Data_data.csv")
    df_fraud=pd.read_csv("data/AxS-Fraud Box_Full Data_data.csv")
    df_median = pd.read_csv("data/AxS-Median Box_Full Data_data (1).csv")
    df_loss = pd.read_csv("data/AxS-Losses Box_Full Data_data.csv")
    df_continental=pd.read_csv("data/AxS-Continental_Full Data_data.csv")

    #dispalay filters and map
    display_map(df_continental,year,quarter)

    #display metrics

    st.subheader(f"{state_name} {report_type} Facts" )
    col1,col2,col3 =st.columns(3)
    with col1:
        display_fraud_facts(df_fraud, year, quarter, state_name, report_type, "State Fraud/Other Count", metric_title,
                            number_format="{:,}")
    with col2:
        display_fraud_facts(df_median, year, quarter, state_name, report_type, "Overall Median Losses Qtr",
                            "Median $ loss", is_median=True)
    with col3:
        display_fraud_facts(df_loss, year, quarter, state_name, report_type, "Total Losses", "Total $ loss")
    #Display filters and map

if __name__=="__main__":
    main()

