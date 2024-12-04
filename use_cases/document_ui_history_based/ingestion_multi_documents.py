import os
from dotenv import load_dotenv
from typing import List
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from consts import INDEX_NAME

load_dotenv()

def ingest_docs(document_path: str, progress_callback=None) -> None:
    """
    Ingest documents from a directory or single file into Pinecone vector store.

    Args:
        document_path (str): Path to the document (txt/pdf) or directory containing documents.
        progress_callback (callable): Function to update progress bar in UI.
    """
    try:
        # Detect if the path is a directory or a file
        if os.path.isdir(document_path):
            files = [
                os.path.join(document_path, f)
                for f in os.listdir(document_path)
                if f.endswith(('.txt', '.pdf'))
            ]
            if not files:
                print("No valid files found in the directory.")
                return
        else:
            if document_path.endswith(('.txt', '.pdf')):
                files = [document_path]
            else:
                print("Unsupported file type.")
                return

        print(f"Found {len(files)} files for ingestion.")

        # Initialize loaders and document list
        all_documents = []
        for file in files:
            if file.endswith(".txt"):
                loader = TextLoader(file)
            elif file.endswith(".pdf"):
                loader = PyPDFLoader(file)
            else:
                continue

            raw_documents = loader.load()
            print(f"Loaded {len(raw_documents)} documents from {file}")
            all_documents.extend(raw_documents)

            # Update progress
            if progress_callback:
                progress_callback(min(100, (len(all_documents) / len(files)) * 100))

        print(f"Total documents loaded: {len(all_documents)}")

        # Split documents into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
        )
        split_documents = text_splitter.split_documents(documents=all_documents)
        print(f"Split into {len(split_documents)} chunks.")

        # Embed and store documents into Pinecone
        print(f"Going to insert {len(split_documents)} chunks into Pinecone.")
        embeddings = OpenAIEmbeddings()
        PineconeVectorStore.from_documents(split_documents, embeddings, index_name=INDEX_NAME)
        print("Successfully added documents to Pinecone.")

        # Final progress update
        if progress_callback:
            progress_callback(100)

    except Exception as e:
        print(f"An error occurred during ingestion: {str(e)}")
        if progress_callback:
            progress_callback(-1)  # Indicate an error

if __name__ == "__main__":
    ingest_docs("path/to/your/documents")
