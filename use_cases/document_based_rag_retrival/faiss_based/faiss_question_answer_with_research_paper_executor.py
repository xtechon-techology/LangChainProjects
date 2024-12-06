from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

load_dotenv()

def pdf_embeddings_faiss(pdf_path:str):
    # pdf_path = "use_cases/document_based_rag_retrival/faiss_based/resources/react.pdf"
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index_react")

    return embeddings




def chat_with_pdf(embeddings: OpenAIEmbeddings, question:str):

    new_vectorstore = FAISS.load_local(
        "faiss_index_react", embeddings, allow_dangerous_deserialization=True
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        OpenAI(), retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(
        new_vectorstore.as_retriever(), combine_docs_chain
    )

    res = retrieval_chain.invoke({"input": question})
    print(res["answer"])
    return res


if __name__ == "__main__":
    print("hi")
    pdf_path = "use_cases/document_based_rag_retrival/faiss_based/resources/react.pdf"
    embeddings = pdf_embeddings_faiss(pdf_path)
    question = "What is React?"
    result = chat_with_pdf(embeddings, question)
    print(result)


