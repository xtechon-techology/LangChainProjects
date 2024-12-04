from typing import Set
from backend.core import run_llm
import streamlit as st


st.set_page_config(
    page_title="Langchain Documentation Helper Chatbot",
    page_icon="🤖",
)

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Langchain Documentation Helper Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


# if prompt := st.chat_input():
#
#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)
#

# ========


# st.header("LangChain Udemy Course - Documentation Helper Bot")

# prompt = st.text_input("Prompt", placeholder="Enter your prompt here..")

# if (
#         "chat_answers_history" not in st.session_state
#         and "user_prompt_history" not in st.session_state
#         and "chat_history" not in st.session_state
# ):
#     st.session_state["chat_answers_history"] = []
#     st.session_state["user_prompt_history"] = []
#     st.session_state["chat_history"] = []


# def create_sources_string(source_urls: Set[str]) -> str:
#     if not source_urls:
#         return ""
#     sources_list = list(source_urls)
#     sources_list.sort()
#     sources_string = "Sources:\n"
#     for i, source in enumerate(sources_list):
#         sources_string += f"{i + 1}. {source}\n"
#     return sources_string


if prompt := st.chat_input():
    with st.spinner("Generating response.."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        print(generated_response)  # Log the response for debugging

        # Check if 'context' exists and process the sources
        if "context" in generated_response:
            sources = set(
                [
                    doc.metadata.get("source", "No source available")
                    for doc in generated_response["context"]
                ]
            )
        else:
            sources = set()

        # Format the response with the answer and sources
        if "answer" in generated_response:
            sources_str = create_sources_string(sources)
            formatted_response = f"{generated_response['answer']} \n\n{sources_str}"
        else:
            formatted_response = (
                f"No answer found. \n\n{create_sources_string(sources)}"
            )

        # Update session state for chat history
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(
            ("ai", generated_response.get("answer", "No answer available"))
        )

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)
