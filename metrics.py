import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import branca.colormap
def display_map2(df,year):
    df=df[(df["TIME_PERIOD"]==year)]
    map=folium.Map(location=[24.5,54.3],zoom_start=7.4,scrollWheelZoom=False,tiles="CartoDB positron")
    choropleth = folium.Choropleth(geo_data="data/ae.json",
                                   fill_color="YlOrRd",
                                   data=df,
                                   highlight=True,
                                   columns=("Reference area","Total"),
                                   key_on="feature.properties.name",
                                   legend_name='Legend',
                                   line_opacity=0.5)
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
    colormap = colormap.to_step(index=[0, 50, 120,180, 230])
    colormap.caption = 'Total number of social organization'
    colormap.add_to(map)
    #colormap = LinearColormap(['yellow', 'orange', 'red'], vmin=0, vmax=100).to_step(10)
    #colormap.add_to(map)

    df=df.set_index("Reference area")
    choropleth.geojson.add_to(map)

    for feature in choropleth.geojson.data['features']:
        emirate = feature["properties"]['name']
        feature["properties"]['Total'] = "Total: " + str("{:,}".format(df.loc[emirate, "Total"]))
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(["name", "Total"], labels=False))
    st_map=st_folium(map,width=700,height=400)


def main():
    df=pd.read_excel("data/output2.xlsx")
    st.write(df["Reference area"].unique())

    df.fillna(0,inplace=True)
    st.write(df["Total"].max())
    st.write(df.head())
    st.write(df.columns)
    year=2022
    display_map(df,year)
if __name__ == '__main__':
    main()
t=1+4
