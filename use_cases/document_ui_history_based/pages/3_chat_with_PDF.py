import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from use_cases.document_based_rag_retrival.faiss_based.faiss_question_answer_with_research_paper_executor import (
    chat_with_pdf,
    pdf_embeddings_faiss,
)

# Page setup
st.set_page_config(
    page_title="Chat with PDF",
    page_icon="🤖",
    layout="wide",
)

# Centered title and description
st.markdown(
    """
    <div style="text-align: center;">
        <h1>💬 Chat with PDF</h1>
        <p>Welcome to the <b>PDF Document-Based Q&A App</b>, developed by Devendra.<br>
        Upload a file to process its content and interact with AI-powered Q&A.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Use columns for left-right alignment for file upload and features
col1, col2 = st.columns([1, 2])

# Left column: Features
with col1:
    st.subheader("🚀 Features:")
    st.markdown(
        """
        - Process documents with embeddings for efficient retrieval.  
        - AI-powered responses based on LangChain and FAISS.  
        - Real-time chat interface.  
        """
    )
    st.markdown("Contact me for custom AI solutions tailored to your needs!")

# Right column: File Upload
with col2:
    st.subheader("📂 Upload File")
    uploaded_file = st.file_uploader(
        "Upload a file (.txt or .pdf):",
        type=["txt", "pdf"],
    )
    if st.button("Process File") and uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            embeddings = pdf_embeddings_faiss(uploaded_file.name)
            st.session_state["pdf_embeddings"] = embeddings
            st.success(f"File `{uploaded_file.name}` processed successfully! ✅")
        except Exception as e:
            st.error(f"Failed to process the file. Error: {e}")

# Divider for Insights and Chat
st.markdown("---")

# Left-Right layout for Insights and Chat
col3, col4 = st.columns(2)

# Left column: Insights
with col3:
    st.subheader("📊 Insights")
    if st.button("Extract Insights"):
        if st.session_state.get("pdf_embeddings"):
            with st.spinner("Extracting insights..."):
                insights = chat_with_pdf(
                    st.session_state["pdf_embeddings"], "Summarize the document."
                )
                st.markdown("### Insights")
                st.session_state["insights_data"] = insights.get("answer", "No insights available")
                st.write(insights.get("answer", "No insights available"))
        else:
            st.error("Please upload and process a file first.")

    # Display insights if available
    if st.session_state["insights_data"]:
        st.write(st.session_state["insights_data"])
    else:
        st.write("No insights available yet. Extract insights after processing a file.")

# Right column: Chat
with col4:
    st.subheader("💬 Chat with AI")
    prompt = st.text_input("Type your question here:")
    if st.button("Ask Question") and prompt:
        with st.spinner("Generating response..."):
            try:
                embeddings: OpenAIEmbeddings = st.session_state.get("pdf_embeddings")
                generated_response = chat_with_pdf(embeddings, prompt)

                # Display user question and AI response
                st.markdown(f"**You:** {prompt}")
                st.markdown(f"**AI:** {generated_response.get('answer', 'No answer available')}")

            except Exception as e:
                st.error(f"Failed to generate a response. Error: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p><b>Live Demo:</b> <a href="#">Streamlit Hosted App</a>  
        <b>GitHub Repository:</b> <a href="#">View Code</a>  
        <b>Contact me on Upwork for inquiries!</b></p>
        <p>Developed with ❤️ by <b>Devendra</b>. Let's build smarter applications together!</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# import streamlit as st
# from langchain_community.embeddings import OpenAIEmbeddings
# from use_cases.document_based_rag_retrival.faiss_based.faiss_question_answer_with_research_paper_executor import (
#     chat_with_pdf, pdf_embeddings_faiss)
#
# # Page setup
# st.set_page_config(page_title="Chat with PDF", page_icon="🤖", layout="wide")
#
# # Header
# st.title("💬 Chat with PDF")
# st.markdown("""
# Welcome to the **PDF Document-Based Q&A App**, developed by **Devendra**.
# Upload a file to process its content and interact with AI-powered Q&A.
#
# ### 🚀 Features:
# - Process documents with embeddings for efficient retrieval.
# - AI-powered responses based on LangChain and FAISS.
# - Real-time chat interface.
# """)
#
# # File upload section
# st.markdown("## 📂 Upload File")
# col1, col2 = st.columns([3, 1], gap="medium")
# with col1:
#     uploaded_file = st.file_uploader(
#         "Upload a file (.txt or .pdf)", type=["txt", "pdf"], label_visibility="visible"
#     )
# with col2:
#     if st.button("Process File") and uploaded_file:
#         with open(uploaded_file.name, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         try:
#             embeddings = pdf_embeddings_faiss(uploaded_file.name)
#             st.session_state["pdf_embeddings"] = embeddings
#             st.success("File processed successfully! ✅")
#         except Exception as e:
#             st.error(f"Failed to process the file. Error: {e}")
#
# st.markdown("---")
#
# # Tabbed Interface for Insights and Chat
# tab1, tab2 = st.tabs(["📄 Insights", "💬 Chat"])
#
# # Insights Tab
# with tab1:
#     st.subheader("📄 Extract Insights")
#     if st.button("Extract Insights"):
#         if st.session_state.get("pdf_embeddings"):
#             with st.spinner("Extracting insights..."):
#                 insights = chat_with_pdf(
#                     st.session_state["pdf_embeddings"], "Summarize the document."
#                 )
#                 st.markdown("### Insights")
#                 st.write(insights.get("answer", "No insights available"))
#         else:
#             st.error("Please upload and process a file first.")
#
# # Chat Tab
# with tab2:
#     st.subheader("💬 Chat with AI")
#     if st.session_state.get("pdf_embeddings"):
#         user_prompt = st.text_input("Type your question here:")
#         if st.button("Ask Question"):
#             with st.spinner("Generating response..."):
#                 response = chat_with_pdf(st.session_state["pdf_embeddings"], user_prompt)
#                 st.markdown("### Response")
#                 st.write(response.get("answer", "No response available"))
#     else:
#         st.info("Please upload and process a file to start chatting.")
#
# # Footer
# st.markdown("---")
# st.markdown("""
# **Live Demo:** [Streamlit Hosted App](#)
# **GitHub Repository:** [View Code](https://github.com/your-repo)
# Contact me on Upwork for inquiries!
#
# **Developed with ❤️ by Devendra**
# *Let's build smarter applications together!*
# """)
