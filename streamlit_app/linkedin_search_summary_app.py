import streamlit as st
import requests

# Add Linkedin icon to the title
st.set_page_config(page_title="Linkedin Profile Summary App", page_icon="/Users/vishald/Documents/DWL/langchain/LangChainProjects/resources/linkedin-icon-v2.png")

# Add a title with Linkedin icon
st.image("/Users/vishald/Documents/DWL/langchain/LangChainProjects/resources/linkedin-icon-v2.png", width=50)

st.title(" Linkedin Profile Summary App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    # llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    # st.info(llm(input_text))
    st.info("This feature is coming soon!")


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")

    # send rest api request to the fastapi server
    request = requests.post("http://localhost:8000/marketing_server", json={"text": text})

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_response(text)