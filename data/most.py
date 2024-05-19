import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
from pandasai import SmartDataframe
#from pandasai.llm import bamboo_llm
from pandasai.responses.response_parser import ResponseParser
from pandasai.llm import GooglePalm
from pandasai import Agent
import time

load_dotenv()
API_KEY = os.environ.get('PANDASAI_API_KEY')

llm = GooglePalm(api_key="AIzaSyBoIKI2fwaoNy7caJiZi_Cw7d0yzPHr8uI")
#importing csv file and converting it to pandas data frame
df = pd.read_csv("my_analysis.csv")
#st.write(df)


# agent configuration
agent = Agent(df)
prompt_engine = SmartDataframe(df, config={'api_key': API_KEY})
prompt_engine_google = SmartDataframe(df, name = "people of Determination in UAE", description="data set that have specific description of people of determination in the united arab emirates",config={'llm': llm})

#chat_engine
chat_engine = SmartDataframe(df, name = "people of Determination in UAE", description="data set that have specific description of people of determination in the united arab emirates",config={'llm': llm})

#train ai with instruction
agent.train(docs="lorem ipsum")

#train using Q/A training
query = "plot the graph"
response = """
import pandas as pd
import plotly.graph_objs as go
def generate_pod_charts(df, year, emirate, pod_category):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]  # Filter data by year

    if emirate and emirate != "":
        filtered_df = filtered_df[filtered_df['Emirates'] == emirate]  # Filter data by emirate

    if pod_category:
        filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category

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

        g2.title("Description ")
        g2.write("This kd dvknvjbfgkjbgsbglfbfgjk n8595296559+62d5f2hs95g259lfb592hg59bs+3.f9gb59skj3f.b+sl9.bgs9l9gh3.fj95ghjhljfgns")
        charts.append(chart)

    if year and emirate:
        # Chart showing disabled by category over the years in the selected emirate
        emirate_filtered_df = df[df['Emirates'] == emirate]
        chart = go.Figure()
        for col in emirate_filtered_df.columns[4:14]:
            chart.add_trace(go.Scatter(x=emirate_filtered_df['Year'], y=emirate_filtered_df[col], mode='lines', name=col))
        chart.update_layout(title=f'Disabled in {emirate} by POD Category over the Years')
        charts.append(chart)

    if year and pod_category:
        # Chart showing disabled in the selected category over the years
        category_filtered_df = df.groupby('Year').sum().reset_index()
        chart = go.Figure()
        chart.add_trace(go.Scatter(x=category_filtered_df['Year'], y=category_filtered_df[pod_category], mode='lines', name=pod_category))
        chart.update_layout(title=f'{pod_category} over the Years')
        charts.append(chart)

    return charts
chartz = generate_pod_charts(df, year, filtered_emirate, disability_type)
st.plotly_chart(chartz)
"""
agent.train(queries=[query], codes = [response])



#generating text area for prompt entering
prompt = st.text_area("Enter your query")
if st.button("Generate"):
    if prompt:
        with st.spinner("please wait while your query is being processed by SANEDEK AI"):
            # st.write(agent.chat(prompt))
            # # explanation = agent.explain()
            # # st.write(explanation)
            #using either agent or smartdataframe
            st.write(prompt_engine_google.chat(prompt))
    else:
        st.warning("please write your query")