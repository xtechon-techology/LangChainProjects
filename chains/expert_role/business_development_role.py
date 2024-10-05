# Pre-requisite: Install langchain-core and langchain-openai packages
# Pre-requisite: Create OpenAI API key and set it in the environment variable OPENAI_API_KEY

# load the package for loading environment variables
from dotenv import load_dotenv

# load the package langchain core for PromptTemplate & ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# Import data-collections's linkedin-scrapper
# from data_collections.linkedin_scrapper import get_linkedin_company_data

import requests
import json
from dotenv import load_dotenv
import os

# Create a function
#   Parameters: LinkedIn company url
#   Steps:
#     1. Load the environment variables
#     2. Get the API key from the environment variables
#     3. Check if the URL is valid
#     4. Extract the company name from the URL
#     5. Check if the company name json file exists
#     6. If the company name json file exists, return the data from the file
#     7. If the company name json file does not exist, call the Scrapin API
#     8. Save the data in the company name json file
#     9. Return the data from the API
#     10. Print the data
def get_linkedin_company_data(linkedin_url):
    #     1. Load the environment variables
    load_dotenv()
    #     2. Get the API key from the environment variables
    key = os.environ["SCRAPIN_API_KEY"]
    #     3. Check if the URL is valid
    is_url_valid = linkedin_url.startswith("https://www.linkedin.com/company/")
    if not is_url_valid:
        return f"Invalid LinkedIn URL [{linkedin_url}]"

    #     4. Extract the company name from the URL
    #        Example: https://www.linkedin.com/company/data-intelligence-llc/ => data-intelligence-llc
    company_name = linkedin_url.split("/")[-2]

    #     5. Check if the company name json file exists
    is_file_exists = os.path.exists(f"{company_name}.json")

    #     6. If the company name json file exists, return the data from the file
    if is_file_exists:
        print(f"Reading data from {company_name}.json")
        with open(f"{company_name}.json", "r") as file:
            data = json.load(file)
            return data
    else:
        #     7. If the company name json file does not exist, call the Scrapin API
        apiEndPoint = f"https://api.scrapin.io/enrichment/company?apikey={key}&linkedinUrl={linkedin_url}"
        response = requests.request("GET", apiEndPoint)

        #     8. Save the data in the company name json file
        with open(f"{company_name}.json", "w") as file:
            file.write(response.text)

        #     9. Return the data from the API
        return response.text


# Create the main function
if __name__ == "__main__":
    # load environment variables
    load_dotenv()

    # Create summary template for the prompt
    summary_template = """
    You are an expert in business development and lead generation. Based on the following LinkedIn Json company data, craft a personalized cold email targeting decision-makers at a technology company. The email should highlight relevant aspects of their business, establish a connection, and present a clear value proposition to initiate a conversation. The email should be professional, concise, and focused on providing solutions that align with the company’s goals and expertise.
    Company data:
    
    Company Name: [company_name]
    Industry: [industry]
    Employee Count: [employee_count]
    Specialties: [specialties]
    Description: [company_description]
    Headquarters: [headquarters]
    Website: [website]
    Founded: [founded]
    
    Objective: Craft a cold email introducing a service or product that can add value to [company_name]'s current operations, with a focus on data engineering & Software QA services. json data {information}
    """

    # Create PromptTemplate object with the summary template
    prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # Create LLM object with ChatOpenAI model (use correct model name)
    llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")  # Corrected model name

    # Create a chain of PromptTemplate and LLM objects with the user input
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Using data-collections's linkedin-scrapper get the company data
    linkedin_url = "https://www.linkedin.com/company/data-intelligence-llc/"
    company_data = get_linkedin_company_data(linkedin_url)

    # Invoke the chain with the user input (removed temperature here)
    response = chain.invoke(input={"information": company_data})

    # Print the response
    print(response)
