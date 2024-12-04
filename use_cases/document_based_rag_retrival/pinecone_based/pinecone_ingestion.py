import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def txt_file_ingestion(document_path="use_cases/document_based_rag_retrival/pinecone_based/files/mediumblog1.txt") -> None:
    print("Ingesting...")
    loader = TextLoader(file_path=document_path)
    document = loader.load()
    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    print("ingesting...")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["PINECONE_INDEX_NAME"]
    )
    print("finish")


if __name__ == "__main__":
    txt_file_ingestion()
