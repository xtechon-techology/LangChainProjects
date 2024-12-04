from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from schemas.parsers import summary_parser

from data_collections.linkedin_scrapper import get_linkedin_company_data
from agents.linkedin_search_agent import search_profile


def linkedin_summarizer(query: str) -> str:
    linkedin_profile_url = search_profile(query=query)
    print(f"Linkedin Profile URL: {linkedin_profile_url}")
    linkedin_data = get_linkedin_company_data(
        linkedin_url=linkedin_profile_url, mock=True
    )

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    # chain = summary_prompt_template | llm
    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    print(res)


# Create the main function
if __name__ == "__main__":
    load_dotenv()

    print("linkedin_summarizer")
    linkedin_summarizer(query="chetu noida linkedin")
