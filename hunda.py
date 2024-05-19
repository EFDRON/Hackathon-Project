import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
from pandasai import SmartDataframe
#from pandasai.llm import bamboo_llm
#from pandasai.responses.response_parser import ResponseParser
#from pandasai.llm import GooglePalm
from pandasai import Agent
import time

load_dotenv()
API_KEY = os.environ.get('PANDASAI_API_KEY')

#llm = GooglePalm(api_key="AIzaSyBoIKI2fwaoNy7caJiZi_Cw7d0yzPHr8uI")
#importing csv file and converting it to pandas data frame
df = pd.read_csv("data/my_analysis.csv")
#st.write(df)


# agent configuration
agent = Agent(df)


prompt_engine = SmartDataframe(df, config={'api_key': API_KEY})
#prompt_engine_google = SmartDataframe(df, name = "people of Determination in UAE", description="data set that have specific description of people of determination in the united arab emirates",config={'llm': llm})

# chat_engine
# chat_engine = SmartDataframe(df, name = "people of Determination in UAE", description="data set that have specific description of people of determination in the united arab emirates",config={'llm': llm})
#
# train ai with instruction
# agent.train(docs="lorem ipsum")
#
# train using Q/A training
query = "win with me"
response = 'print("hello")'

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
            st.write(agent.chat(prompt))
    else:
        st.warning("please write your query")