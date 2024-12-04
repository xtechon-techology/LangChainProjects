import json
import re

import streamlit as st
from langchain.agents import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load environment variables
os.environ["LANGCHAIN_ALLOW_DANGEROUS_CODE"] = "true"

st.title("Query Database/CSV/Excel with Visualizations")
pick = st.selectbox(
    "Choose Database/CSV/Excel:",
    ("CSV/Excel", "MySQL Database")
)

# pick = st.selectbox(
#     "Choose Database/CSV/Excel:",
#     ("CSV/Excel", "MySQL Database")
# )

# Initialize the language model
llm = ChatOpenAI(temperature=0, model_name="gpt-4")


# MySQL Database Agent
def mysqldb_agent(db, llm, user_input):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    return agent_executor.invoke(user_input)  # Updated from `run` to `invoke`


# CSV/Excel Agent
def csv_excel_agent(df, llm, user_input):
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True
    )
    return agent.invoke(user_input)  # Updated from `run` to `invoke`

def convert_into_json_format_old(input_response: str) -> str:

    summary_template = """
    given the input response {information} with input and output key with json. convert this output key text into json format.
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": input_response})

    print(res)

    return res


def convert_into_json_format(input_response: str) -> dict:
    """
    Extracts and converts the 'output' key text from the given input response into a JSON object.

    Args:
        input_response (str): The response containing JSON text.

    Returns:
        dict: The extracted and parsed JSON object.
    """
    # Template for the LLM to transform the response
    summary_template = """
    Extract the JSON object from the given response text. Only return the JSON object, nothing else.
    
    Input:
    {information}

    Output:
    
    example:
    
    Input : {
"input":"What are the counts with rule_name wise in the given data?"
"output":"The counts of each unique value in the 'rule_name' column are as follows:
- DataTypeRule: 125
- MaxLengthRule: 72
- CompletenessPattern: 72
- MinLengthRule: 70
- CategoricalRangeRule: 68
- Completeness: 53
- PositiveNumRule: 41
- StandardDeviationRule: 27
- Uniqueness: 22
- TimelinessRule: 6
- DateFormatRule: 4
- PatternGUIDRule: 1"
}

  Output : {
    "DataTypeRule": 125,
    "MaxLengthRule": 72,
    "CompletenessPattern": 72,
    "MinLengthRule": 70,
    "CategoricalRangeRule": 68,
    "Completeness": 53,
    "PositiveNumRule": 41,
    "StandardDeviationRule": 27,
    "Uniqueness": 22,
    "TimelinessRule": 6,
    "DateFormatRule": 4,
    "PatternGUIDRule": 1
}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": input_response})


    # Convert the extracted JSON string into a dictionary
    # try:
    #     json_output = json.loads(response)
    # except json.JSONDecodeError:
    #     raise ValueError("Failed to decode JSON from the response. Please check the input format.")

    return response


def extract_json_from_text(content: str) -> dict:
    """
    Extracts the JSON object from the given content by finding the first valid JSON-like structure.

    Args:
        content (str): The string containing the JSON object.

    Returns:
        dict: The extracted JSON object.

    Raises:
        ValueError: If no valid JSON object is found.
    """
    start_idx = content.find("{")  # Find the first opening brace
    end_idx = content.rfind("}")  # Find the last closing brace

    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise ValueError("No JSON object found in the content.")

    # Extract the potential JSON substring
    json_str = content[start_idx:end_idx + 1]

    try:
        # Parse the extracted substring as JSON
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}")

def convert_list_to_json(input_response: str) -> dict:
    """
    Extracts the 'output' section from the input and converts the listed items into a JSON object.

    Args:
        input_response (str): The response containing rules as text.

    Returns:
        dict: The extracted and structured JSON object.
    """
    # Regular expression to isolate the 'output' section
    match = re.search(r'"output":"([^"]+)"', input_response, re.DOTALL)
    if not match:
        raise ValueError("No 'output' section found in the input.")

    # Extract the 'output' text
    output_text = match.group(1).replace("\\n", "\n")

    # Convert the listed items into a JSON object
    json_object = {}
    lines = output_text.split("\n")
    for line in lines:
        # Match lines with the format "- Key: Value"
        if match := re.match(r"- (\w+): (\d+)", line.strip()):
            key, value = match.groups()
            json_object[key] = int(value)

    if not json_object:
        raise ValueError("Failed to parse any key-value pairs from the 'output' section.")

    return json_object


# Visualization function
def show_chart(data, title="Chart"):
    try:
        if isinstance(data, pd.DataFrame):
            st.write(data)  # Display the DataFrame
            # Show as a bar chart
            st.bar_chart(data)
        elif isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["Key", "Value"])
            st.write(df)
            sns.barplot(x="Key", y="Value", data=df)
            plt.title(title)
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.write(data)
    except Exception as e:
        st.error(f"Error visualizing data: {str(e)}")


# MySQL Database Option
if pick == 'MySQL Database':
    st.subheader("Query MySQL Database:")
    db_user = st.text_input("Username:", "admin")
    db_password = st.text_input("Password:", "admin", type="password")
    db_host = st.text_input("Host:", "localhost")
    db_name = st.text_input("Database Name:", "matrix")

    if st.button("Connect to Database"):
        try:
            db = SQLDatabase.from_uri(
                f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
            )
            print(db.dialect)
            print(db.get_usable_table_names())
            st.success("Database connection successful!")
            input_text = st.text_input("Enter your question here:",
                                       "What are total trade transactions strategy wise in matrix.trade_transactions table?")
            if st.button("Generate Response"):
                with st.spinner("Generating response..."):
                    reply = mysqldb_agent(db, llm, input_text)
                    print(reply)
                st.success("Response:")
                show_chart(reply)
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
                st.success("Response:")
                st.write(reply)




