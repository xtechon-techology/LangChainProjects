import streamlit as st
from use_cases.document_ui_history_based.ingestion_multi_documents import ingest_docs

# Configure the Streamlit page
st.set_page_config(
    page_title="Multi File Q&A with OpenAI",
    page_icon="📝",
    layout="centered"
)

# Title and description
st.title("📝Multi Document Based Q&A with OpenAI")
st.markdown(
    """
    Welcome to the **Document Based Q&A App**!  
    Upload a file or provide a directory path to process and analyze your documents.
    """
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload a single file (.txt or .pdf):",
    type=["txt", "pdf"],
    label_visibility="visible",
)

# Directory path input
st.markdown("---")
st.subheader("Process Documents via Directory Path")
directory_path_provided = st.text_input("Enter the directory path:")

# Progress and Status Handling
if st.button("Submit Directory Path"):
    if directory_path_provided:
        st.success(f"Directory path submitted: `{directory_path_provided}`")
        progress_bar = st.progress(0)

        def update_progress(progress):
            progress_bar.progress(progress if progress >= 0 else 0)  # Ensure valid range

        ingest_docs(directory_path_provided, progress_callback=update_progress)

        st.success("Document ingestion completed! ✅")
    else:
        st.error("Please enter a valid directory path.")

# Process Uploaded File
if uploaded_file:
    st.markdown("---")
    st.subheader("Processing Uploaded File")
    file_path = uploaded_file.name

    with st.spinner(f"Processing `{file_path}`..."):
        ingest_docs(document_path=file_path)

    st.success(f"File `{file_path}` processed successfully! ✅")

# Footer
st.markdown("---")
st.markdown(
    """
    **Developed by Devendra with ❤️ using Streamlit.**  
    Powered by Anthropic for smarter document processing.
    """
)
