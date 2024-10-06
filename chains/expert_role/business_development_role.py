# Pre-requisite: Install langchain-core and langchain-openai packages
# Pre-requisite: Create OpenAI API key and set it in the environment variable OPENAI_API_KEY

# load the package for loading environment variables
from dotenv import load_dotenv

# load the package langchain core for PromptTemplate & ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# Import data-collections's linkedin-scrapper
from data_collections.linkedin_scrapper import get_linkedin_company_data


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
