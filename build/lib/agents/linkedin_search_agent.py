
import sys
from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub

def search_profile(query: str) -> str:
    llm = ChatOpenAI(temperature=0,  model="gpt-4o-mini")

    template = """ given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    Your answer should contain only a URL."""

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    tools_for_agent = [
        Tool(
            name="search_profile",
            func=get_profile_url_tavily,
            description="Search for a person's profile on Linkedin"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    response = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=query)}
    )

    linkedin_url = response["output"]
    return linkedin_url


if __name__ == "__main__":
    profile_url = search_profile("DoWhileLearn linkedin")