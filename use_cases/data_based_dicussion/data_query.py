import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

import pandas as pd
import os

# Load environment variables
load_dotenv()

# Enable dangerous code execution in LangChain explicitly via environment variable
os.environ["LANGCHAIN_ALLOW_DANGEROUS_CODE"] = "true"

st.title("How to Query Database/CSV/Excel?")
pick = st.selectbox(
    "Choose Database/CSV/Excel:",
    ("CSV/Excel", "MySQL Database")
)

# Initialize the language model
llm = ChatOpenAI(temperature=0, model_name="gpt-4")


# MySQL Database Agent
def mysqldb_agent(db, llm, user_input):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    return agent_executor.run(user_input)


# CSV/Excel Agent
def csv_excel_agent(df, llm, user_input):
    # Enable dangerous code execution explicitly
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True  # This is the key fix for the error
    )
    return agent.run(user_input)


# MySQL Database Option
if pick == 'MySQL Database':
    st.subheader("Query MySQL Database:")
    db_user = st.text_input("Username:", "root")
    db_password = st.text_input("Password:", "root", type="password")
    db_host = st.text_input("Host:", "localhost")
    db_name = st.text_input("Database Name:", "bankdata")

    if st.button("Connect to Database"):
        try:
            db = SQLDatabase.from_uri(
                f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
            )
            st.success("Database connection successful!")
            input_text = st.text_input("Enter your question here:",
                                       "What is the maximum transaction in the database table?")
            if st.button("Generate Response"):
                with st.spinner("Generating response..."):
                    reply = mysqldb_agent(db, llm, input_text)
                st.write(reply)
        except Exception as e:
            st.error(f"Error connecting to the database: {str(e)}")

# CSV/Excel Option
elif pick == 'CSV/Excel':
    st.subheader("Using CSV/Excel:")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        st.success("File uploaded successfully!")
        try:
            # Load file into a DataFrame
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            df = None

        if df is not None:
            st.write("Preview of the uploaded data:")
            st.dataframe(df.head())

            input_text = st.text_input("Enter your question here:",
                                       "What are the counts with rule_name wise in the given data?")
            if st.button("Generate Response"):
                with st.spinner("Generating response..."):
                    reply = csv_excel_agent(df, llm, input_text)
                st.write(reply)
