# Pre-requisite: Install langchain-core and langchain-openai packages
# Pre-requisite: Create OpenAI API key and set it in the environment variable OPENAI_API_KEY

# load the package for loading environment variables
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

# load the package langchain core for PromptTemplate & ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_ollama import ChatOllama

# Create user input variable for the prompt
input_data = "What is the capital of France?"

# Create the main function
if __name__ == "__main__":
    # load environment variables
    load_dotenv()

    # Create summary template for the prompt
    summary_template = """
    Given the information: {information} about the person, I want you to create:
    1. A short summary of the person
    2. Two interesting facts about the person
    """

    # Create PromptTemplate object with the summary template
    prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # Create LLM object with ChatOpenAI model (use correct model name)
    # llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")  # Corrected model name
    llm = ChatOllama(model="mistral")

    # Create a chain of PromptTemplate and LLM objects with the user input
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain with the user input (removed temperature here)
    response = chain.invoke(input={"information": input_data})

    # Print the response
    print(response)
