from typing import Set

from langchain_core.runnables.utils import Output
from langchain_openai import OpenAIEmbeddings, OpenAI

from backend.core import run_llm
import streamlit as st

from use_cases.document_based_rag_retrival.faiss_based.faiss_question_answer_with_research_paper_executor import \
    chat_with_pdf

st.set_page_config(
    page_title="Langchain Documentation Helper Chatbot",
    page_icon="🤖",
)


st.title("💬 Langchain Documentation Helper Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
# radio button to select the chat with pdf/text or with the document
chat_with = st.radio("Select the chat with", ["pdf/text", "document"])

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string



if prompt := st.chat_input():
    sources: set = set()
    generated_response: Output
    with st.spinner("Generating response.."):
        if chat_with == "pdf/text":
            embeddings: OpenAIEmbeddings = st.session_state.get("pdf_embeddings")
            formatted_response = chat_with_pdf(embeddings, prompt)
            print(formatted_response)

        if chat_with == "document":

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
