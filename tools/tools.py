from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(query: str):
    search = TavilySearchResults()
    result = search.run(f"{query}")
    return result
