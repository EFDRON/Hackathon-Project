import os
import pandas as pd
from pandasai import PandasAI
import streamlit as st
from pandasai.llm.openai import OpenAI
#os.environ["PANDASAI_API_KEY"] = "$2a$10$YTXHA8WRvLcyg6TQHhzVke7RvdvdCTrTTlM/7R1jpWbQWWTPM0Oy6"

"""agent = Agent(df)
females=df[df["Sex"]=="female"]
st.write(females["Survived"].sum()/len(females))
question="What can you tell us about the class of the passengers? is there a correlation with survival rate?"
question2="what exactly is the survival rate of higher passengers?"
response=agent.chat(question)
respnse2=agent.chat(question2)

st.write(response)
st.write(respnse2)"""

df=pd.read_csv("data/titanic.csv")
llm=OpenAI(api_token="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")
pandas_ai=PandasAI(llm)
pandas_ai.run(df,prompt="What sex was most likely to have survived?")