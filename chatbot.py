import streamlit as st
st.title("CHATBOT Practice")
chat_placeholder=st.container()
prompt_placeholder=st.form("chat_form")
with prompt_placeholder:
    st.markdown("**Chat** _Press Enter to Submit")
    cols=st.columns((6,1))
    cols[0].text_input("Chat",value="Hello Bot",label_visibility="collapsed")
    cols[1].form_submit_button("submit",type="primary")