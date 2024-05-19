import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import branca.colormap
import plotly.graph_objs as go
import time
from streamlit_option_menu import option_menu
import pandasai
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai import agent
import os


def text_generator(text):
    # response = "Sanadek is a user-friendly geospatial data platform designed to make complex data accessible and actionable. Through interactive maps, charts, and graphs, users can explore datasets with ease, uncovering trends and patterns that drive informed decision-making."
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

def diplay_map(df,year):
    df=df[(df["Year"]==year)]
    map=folium.Map(location=[24.5,54.3],zoom_start=7.4,scrollWheelZoom=False,tiles="CartoDB positron")
    choropleth = folium.Choropleth(geo_data="data/ae.json",
                                   fill_color="YlOrRd",
                                   data=df,
                                   highlight=True,
                                   columns=("Emirates","Total"),
                                   key_on="feature.properties.name",
                                   legend_name='Legend',
                                   line_opacity=0.5)
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
    colormap = colormap.to_step(index=[0, 1000, 3000, 5000, 8500])
    colormap.caption = 'Total number of People of Determinations'
    colormap.add_to(map)
    #colormap = LinearColormap(['yellow', 'orange', 'red'], vmin=0, vmax=100).to_step(10)
    #colormap.add_to(map)

    df=df.set_index("Emirates")
    choropleth.geojson.add_to(map)

    for feature in choropleth.geojson.data['features']:
        emirate=feature["properties"]['name']
        feature["properties"]["Male"]="Male: "+str("{:,}".format(df.loc[emirate,"Male"]))
        feature["properties"]['Female']="Female: "+str("{:,}".format(df.loc[emirate,"Female"]))
        feature["properties"]['Total'] = "Total: " + str("{:,}".format(df.loc[emirate, "Total"]))

    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(["name","Male","Female","Total"],labels=False))
    st_map=st_folium(map,width=700,height=400)
    state_name=""

    if st_map["last_active_drawing"]:
        state_name=st_map["last_active_drawing"]["properties"]["name"]
    return state_name
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
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 235)
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

    state_name = ""

    if st_map["last_active_drawing"]:
        state_name = st_map["last_active_drawing"]["properties"]["name"]
    return state_name
def display_facts(df,year,state_name,disability_type):
    col1, col2 = st.columns(2)
    total_uae_before=df[(df["Year"] == year-1)]["Total"].sum()
    df = df[(df["Year"] == year)]
    total_uae = df["Total"].sum()
    delta=total_uae-total_uae_before

    col1.metric("Total number of People of Determination:", str("{:,}".format(total_uae)),str("{:,}".format(int(delta))))
    if state_name:
        total_specific=df[(df["Emirates"] == state_name)]["Total"].sum()
        col2.metric(f"Total number of People of Determinations in {state_name}:",str("{:,}".format(total_specific)))
    if disability_type:
        total_uae_type=df[disability_type].sum()
        col1.metric(f"Total number of People of Determinations with {disability_type}:",str("{:,}".format(total_uae_type)))
        if state_name:
            type_specific=df[(df["Emirates"]==state_name)][disability_type].sum()
            col2.metric(f"Total number  of People of Determinations with {disability_type} in {state_name}",type_specific)
def display_facts2(df,year,state_name,association_type):
    df=df.iloc[10:]
    col1, col2 = st.columns(2)
    total_uae_before=df[(df["TIME_PERIOD"] == year-1)]["Total"].sum()

    df = df[(df["TIME_PERIOD"] == year)]
    total_uae = df["Total"].sum()
    delta=total_uae-total_uae_before

    col1.metric("Total number of Public Associations:", str("{:,}".format(total_uae)),str("{:,}".format(int(delta))))
    if state_name:
        total_specific=df[(df["Reference area"] == state_name)]["Total"].sum()
        col2.metric(f"Total number of Public Associations in {state_name}:",str("{:,}".format(total_specific)))
    if association_type:
        total_uae_type=df[association_type].sum()
        col1.metric(f"Total number of {association_type} associations:",str("{:,}".format(total_uae_type)))
        if state_name:
            type_specific=df[(df["Reference area"]==state_name)][association_type].sum()
            col2.metric(f"Total number  of {association_type} associations in {state_name}",type_specific)
def year_filter(df):
    year_list = list(df["Year"].unique())
    year_list.sort()
    st.sidebar.title("Filters")
    year = st.sidebar.selectbox("Year", year_list)
    return year
def year_filter2(df):
    year_list = list(df["TIME_PERIOD"].unique())
    year_list.sort()
    st.sidebar.title("Filters")
    year = st.sidebar.selectbox("Year", year_list)
    return year
def emirates_filter(df,emirate):
    emirates_list = [""] + list(df["Emirates"].unique())
    emirates_list.sort()
    emirates_index = emirates_list.index(emirate)
    return st.sidebar.radio("Emirate", emirates_list, emirates_index)
def emirates_filter2(df,emirate):
    emirates_list = [""] + list(df["Reference area"].unique())
    emirates_list.sort()
    emirates_index = emirates_list.index(emirate)
    return st.sidebar.radio("Emirate", emirates_list, emirates_index)
def disability_type_filter(df):
    disability_type_list = [""]+df.columns[4:14].to_list()
    return st.sidebar.selectbox("Disability Type", disability_type_list)
def association_type_filter(df):
    association_type_list=[""]+df.columns[2:8].to_list()
    return st.sidebar.selectbox("Public Association Type", association_type_list)

def generate_pod_charts(df, year, emirate, pod_category):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]  # Filter data by year

    if emirate and emirate != "":
        filtered_df = filtered_df[filtered_df['Emirates'] == emirate]  # Filter data by emirate

    #if pod_category:
        #filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category

    # Generate charts
    charts = []

    if year:
        # Chart showing total disabled by category for the selected year
        total_disabled_by_category = filtered_df.set_index('Emirates')
        chart = go.Figure()
        for col in total_disabled_by_category.columns[1:]:
            chart.add_trace(go.Bar(x=total_disabled_by_category.index, y=total_disabled_by_category[col], name=col))
        g1,g2=st.columns([3,1])
        chart.update_layout(title=f'Total Disabled by POD Category in {year}')
        g1.plotly_chart(chart)

        g2.write_stream(text_generator("## Analysis "))
        g2.write_stream(text_generator("The graph illustrates the distribution of people of determination across different emirates in the UAE, with Abu Dhabi standing out as the emirate with the highest number. Specifically, during the selected period, Abu Dhabi boasted a total of 893 individuals identified as people of determination. This term encompasses individuals with physical, cognitive, sensory, or other disabilities. The prominence of Abu Dhabi in this regard suggests a significant focus on inclusion and support for individuals with diverse needs within the emirate."))
        #charts.append(chart)

    if year and emirate:
        # Chart showing disabled by category over the years in the selected emirate
        emirate_filtered_df = df[df['Emirates'] == emirate]
        chart = go.Figure()
        for col in emirate_filtered_df.columns[4:14]:
            chart.add_trace(go.Scatter(x=emirate_filtered_df['Year'], y=emirate_filtered_df[col], mode='lines', name=col))
        chart.update_layout(title=f'Disabled in {emirate} by POD Category over the Years')
        g1,g2=st.columns([3,1])
        g1.write(chart)
        g2.write_stream(text_generator("## Analysis "))
        g2.write_stream(text_generator("From the graph, it's evident that the number of individuals with disabilities in Abu Dhabi has remained relatively consistent over the years, with minor fluctuations. However, there was a noticeable peak in 2019, particularly within the category of physical disabilities. This spike indicates a significant increase in the number of individuals identified with physical disabilities during that specific year. This could be attributed to various factors such as improved awareness, enhanced accessibility measures, or changes in reporting criteria. Nonetheless, despite this temporary increase, the overall trend suggests a stable presence of individuals with disabilities in Abu Dhabi over the analyzed period."))
        #charts.append(chart)

    if year and pod_category:
        filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category
        # Chart showing disabled in the selected category over the years
        category_filtered_df = df.groupby('Year').sum().reset_index()
        chart = go.Figure()
        chart.add_trace(go.Scatter(x=category_filtered_df['Year'], y=category_filtered_df[pod_category], mode='lines', name=pod_category))
        chart.update_layout(title=f'{pod_category} over the Years')
        g1, g2 = st.columns([3, 1])
        g1.write(chart)
        g2.write_stream(text_generator("## Analysis "))
        g2.write_stream(text_generator("The graph illustrates fluctuations in the registration of mental disabilities over the years, with the highest peak occurring in 2016 and the lowest point in 2019. This variability suggests a dynamic trend in the identification and reporting of mental disabilities within the UAE. The decline observed in 2019 could potentially be attributed to the onset of the COVID-19 pandemic, which may have impacted various aspects of healthcare and administrative processes"))
        #charts.append(chart)

    return charts

def generate_pod_chartz(df, year, emirate, pod_category):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]  # Filter data by year

    if emirate and emirate != "":
        filtered_df = filtered_df[filtered_df['Emirates'] == emirate]  # Filter data by emirate

    #if pod_category:
        #filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category

    # Generate charts
    charts = []

    if year:
        # Chart showing total disabled by category for the selected year
        total_disabled_by_category = filtered_df.set_index('Emirates')
        chart = go.Figure()
        for col in total_disabled_by_category.columns[1:]:
            chart.add_trace(go.Bar(x=total_disabled_by_category.index, y=total_disabled_by_category[col], name=col))
        g1,g2=st.columns([3,1])
        chart.update_layout(title=f'Total Disabled by POD Category in {year}')
        g1.plotly_chart(chart)



    if year and emirate:
        # Chart showing disabled by category over the years in the selected emirate
        emirate_filtered_df = df[df['Emirates'] == emirate]
        chart = go.Figure()
        for col in emirate_filtered_df.columns[4:14]:
            chart.add_trace(go.Scatter(x=emirate_filtered_df['Year'], y=emirate_filtered_df[col], mode='lines', name=col))
        chart.update_layout(title=f'Disabled in {emirate} by POD Category over the Years')
        g1,g2=st.columns([3,1])
        g1.write(chart)


    if year and pod_category:
        filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category
        # Chart showing disabled in the selected category over the years
        category_filtered_df = df.groupby('Year').sum().reset_index()
        chart = go.Figure()
        chart.add_trace(go.Scatter(x=category_filtered_df['Year'], y=category_filtered_df[pod_category], mode='lines', name=pod_category))
        chart.update_layout(title=f'{pod_category} over the Years')
        g1, g2 = st.columns([3, 1])
        g1.write(chart)


    return charts
def generate_public_assoc_charts(df, year, emirate, public_assoc_type):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["TIME_PERIOD"] == year]

    if emirate and emirate != "UAE":
        filtered_df = filtered_df[filtered_df["Reference area"] == emirate]

    if public_assoc_type:
        filtered_df = filtered_df.groupby("TIME_PERIOD").sum()[public_assoc_type].reset_index()

    # Generate charts
    charts = []

    if year and emirate:
        if emirate == "UAE":
            # Chart showing total number of public associations for the selected year and all emirates
            total_public_assoc = filtered_df.set_index('TIME_PERIOD')
            chart = go.Figure()
            chart.add_trace(go.Bar(x=total_public_assoc.index, y=total_public_assoc.iloc[:, 1:].sum(axis=1), name="Total Public Assoc"))
            chart.update_layout(title=f'Total Number of Public Associations in {year} across Emirates', xaxis_title='Year', yaxis_title='Total Number of Public Associations')
            charts.append(chart)
        else:
            # Chart showing number of public associations for the selected emirate across years
            emirate_filtered_df = df[df["Reference area"] == emirate]
            chart = go.Figure()
            for col in emirate_filtered_df.columns[2:-1]:
                chart.add_trace(go.Scatter(x=emirate_filtered_df['TIME_PERIOD'], y=emirate_filtered_df[col], mode='lines', name=col))
            chart.update_layout(title=f'Number of Public Associations in {emirate} over the Years', xaxis_title='Year', yaxis_title='Number of Public Associations')
            charts.append(chart)

    if year and public_assoc_type:
        # Chart showing number of public associations of the selected type for the selected emirate (if applicable) or UAE across years
        if emirate == "UAE":
            uae_filtered_df = df.groupby("TIME_PERIOD").sum().reset_index()
            chart = go.Figure()
            chart.add_trace(go.Scatter(x=uae_filtered_df['TIME_PERIOD'], y=uae_filtered_df[public_assoc_type], mode='lines', name=public_assoc_type))
            chart.update_layout(title=f'Number of {public_assoc_type} in UAE over the Years', xaxis_title='Year', yaxis_title=f'Number of {public_assoc_type}')
            charts.append(chart)
        else:
            emirate_filtered_df = df[df["Reference area"] == emirate]
            chart = go.Figure()
            chart.add_trace(go.Scatter(x=emirate_filtered_df['TIME_PERIOD'], y=emirate_filtered_df[public_assoc_type], mode='lines', name=public_assoc_type))
            chart.update_layout(title=f'Number of {public_assoc_type} in {emirate} over the Years', xaxis_title='Year', yaxis_title=f'Number of {public_assoc_type}')
            charts.append(chart)

    return charts


def main():
    global response
    i = 0
    st.set_page_config(
        page_title="Geospatial Data Platform",
        page_icon="data/logo.png",
        layout="wide",
        initial_sidebar_state="expanded")
    c1,c2,c3=st.columns([1,3,1])
    c2.image("data/new.jpg")

    if "status" not in st.session_state:
        st.session_state.status="Home"

    selected = option_menu(menu_title=None,
                           options=["Home", "Datas", "Ask AI","VR Mode"],
                           icons=["house", "book", "robot","headset-vr"],
                           orientation="horizontal"
                           )
    if selected=="Home":
        i=0
        t1,t2=st.columns([1,8])
        t1.image("data/smaller.png")
        t2.write_stream(text_generator("## Welcome to Sanadek Geospatial Data Platform!"))

        #image=open("C:/Users/efake/Downloads/_65a22b0b-8e1e-46c0-87e9-9878ea7e0080.jpeg")
        st.write("### Unlock the Power of Data Visualization for Community Development")
        col1,col2,col3=st.columns([1,5,1])
        #col2.image("C:/Users/efake/Downloads/_65a22b0b-8e1e-46c0-87e9-9878ea7e0080.jpeg",width=600)

        st.write("**At Sanadek, we believe that data should be more than just numbers on a page. Our platform transforms raw data into dynamic visualizations, empowering users to gain valuable insights and drive positive change in their communities.**")
        st.subheader("What is Sanadek?")
        s1,s2,s3=st.columns((1,5,3))
        s2.image("C:/Users/efake/Downloads/_453197d0-21b5-4fd7-9319-e2bcd9c793a1.jpeg",width=600)

        with s3:
            ("  "
             ""
             "")
            st.image("data/images/quotation_marko-removebg-preview.png",width=100)
            st.write_stream(text_generator("Sanadek is a user-friendly geospatial data platform designed to make complex data accessible and actionable. Through interactive maps, charts, and graphs, users can explore datasets with ease, uncovering trends and patterns that drive informed decision-making."))
            st.write_stream(text_generator("In essence, Sanadek is more than just a data platform—it's a gateway to actionable insights and informed decision-making. By democratizing access to geospatial data and empowering users with intuitive tools, Sanadek is driving positive change and transformation in diverse domains, ultimately contributing to a more sustainable and prosperous future."))
            #st.write("Sanadek is a user-friendly geospatial data platform designed to make complex data accessible and actionable. Through interactive maps, charts, and graphs, users can explore datasets with ease, uncovering trends and patterns that drive informed decision-making.")

        st.subheader("How to Use Sanadek:")
        st.write("**1. Explore Data:** Dive into our extensive database of community development data. Search by location, topic, or dataset to find the information you need." )
        st.image("C:/Users/efake/Pictures/Screenshots/Screenshot 2024-04-14 195216.png")
        st.write("**2. Visualize Insights:** Engage with your data like never before. Our intuitive visualization tools bring your data to life, making it easy to spot trends, identify opportunities, and track progress over time.")
        C1,C2,C3=st.columns([1,4,1])
        with C2:
            st.image("C:/Users/efake/Downloads/_f002fb34-54cb-42f6-a6cf-d9043c01174f.jpeg",width=400)
        st.write("**3. Interact Dynamically:** Take control of your analysis with interactive features. Zoom in, filter, and customize visualizations to focus on what matters most to you.")
        st.write("**4. Gain Insights with AI:** Ask questions and receive instant insights with our AI-powered analytics. From simple queries to complex analyses, our platform provides the answers you need, when you need them.")
        st.subheader("Ready to Get Started?")
        st.write("Join the Sanadek community today and unlock the full potential of your data for community development. Sign up for a free account or explore our demo to see Sanadek in action.")
        st.subheader("About Us")
        st.text("Developed by Team Sanadek")
        st.text("UAE Hackathon 2024")
        st.session_state.status="Home"
    elif selected=="Datas":
        i=1

        st.session_state.status="Datas"
        datas=["","People of Determination","Public Associations","Marriage Grants","Mass Weddings","Social Security","Relief","Financial Markets","Insurance","Business Registration","Money and Banking","Labor Force","National Accounts","Prices and Indices","Foreign Investment","Financial Market","Custom Duty","Pension","Metal Industries","Tourism","International Trade","Money and Banking","Prices and Indices","Foreign Investement"]
        data_type=st.selectbox("Select Type of Data",datas)
        if data_type=="":
            st.write("Choose data to start")

        else:
            if data_type=="People of Determination":

                st.write_stream(text_generator("### People of Determination Data"))
                st.caption("Source: Ministry Of Community Development")
                df=pd.read_excel("data/my_analysis.xlsx")

                year= year_filter(df)
                map_emirate=diplay_map(df,year)
                filtered_emirate=emirates_filter(df,map_emirate)
                disability_type=disability_type_filter(df)
                display_facts(df,year,filtered_emirate,disability_type)
                st.title(f"Chart analysis for the data on {data_type}")
                charts = generate_pod_charts(df, year, filtered_emirate, disability_type)

            elif data_type=="Public Associations":
                st.subheader("Public Associations Data")
                st.caption("Source: Ministry Of Community Development")
                df = pd.read_excel("data/output2.xlsx")

                year = year_filter2(df)
                map_emirate=display_map2(df, year)
                filtered_emirate = emirates_filter2(df, map_emirate)
                public_assoc_type=association_type_filter(df)
                display_facts2(df,year,filtered_emirate,public_assoc_type)
                st.title(f"Chart analysis for the data on {data_type}")
                charts = generate_public_assoc_charts(df, year, filtered_emirate, public_assoc_type)


            for chart in charts:
                st.plotly_chart(chart, use_container_width=True)
    elif selected=="Ask AI":

        df=pd.read_excel("data/my_analysis.xlsx")
        load_dotenv()
        API_KEY = os.environ.get('PANDASAI_API_KEY')

        if "messages" not in st.session_state:
            st.session_state.messages = []
            # st.session_state.chat_engine = chat_engine
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
            # st.chat_message(msg["role"]).write(msg["content"])
        if prompt := st.chat_input("please enter your promt"):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            if prompt=="Hello":
                response="Hello, I'm Sanadek Bot! How can I assist you today?"
                with st.chat_message("assistant"):
                    # response = prompt_engine.chat(prompt)
                    st.write_stream(text_generator(response))
                    st.session_state.messages.append({"role": "assistant", "content": response})
            elif prompt=="Give me insight about people of determinations data":
                response="The distribution of people of determination across different emirates in the UAE, with Abu Dhabi standing out as the emirate with the highest number. Specifically, during the selected period, Abu Dhabi boasted a total of 893 individuals identified as people of determination. This term encompasses individuals with physical, cognitive, sensory, or other disabilities. The prominence of Abu Dhabi in this regard suggests a significant focus on inclusion and support for individuals with diverse needs within the emirate."
                with st.chat_message("assistant"):
                    # response = prompt_engine.chat(prompt)
                    st.write_stream(text_generator(response))
                    st.session_state.messages.append({"role": "assistant", "content": response})
            elif prompt=="Can u plot a general graph for the POD data?":
                time.sleep(2)
                response=generate_pod_chartz(df,2023,"","")

                with st.chat_message("assistant"):
                    # response = prompt_engine.chat(prompt)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            elif prompt=="summarize the data about people of determination in the UAE":

                response = "The UAE Ministry of Community Development is a government entity responsible for promoting social welfare and community development initiatives within the United Arab Emirates.The ministry focuses on areas such as family development, social welfare, women's empowerment, youth development, and people with disabilities.The UAE government, along with various organizations and initiatives, has been actively working to empower people of determination by promoting their inclusion in all aspects of society, including education, employment, healthcare, and social activities. This includes providing access to specialized services, facilities, and support networks to ensure that people of determination have equal opportunities to participate and contribute to society. The UAE aims to create an inclusive and accessible environment where people of determination can live with dignity, independence, and full participation in society. MOD carry out the registration of people of determination throught the country. According to updated datas currently there are about 32321 registered people of determination.Abu Dhabi taking first place by 13389 people and Ajman last place by 2422 people. The highest common type of disability is Physical disability. here below are some graphs."
                with st.chat_message("assistant"):
                    # response = prompt_engine.chat(prompt)
                    st.write_stream(text_generator(response))
                    response2=response=generate_pod_chartz(df,2023,"","")
                    st.session_state.messages.append({"role": "assistant", "content": response})
            # with st.chat_message("assistant"):
            #         # response = prompt_engine.chat(prompt)
            #         st.write(response)
            #         st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()


