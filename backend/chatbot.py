from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, CSVLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


# 1. Load documents
def load_documents(folder_path):
    docs = []
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if fname.endswith(".txt"):
            docs += TextLoader(full_path).load()
        elif fname.endswith(".pdf"):
            docs += PyPDFLoader(full_path).load()
        elif fname.endswith(".csv"):
            docs += CSVLoader(full_path).load()
    return docs

# 2. Create Vector DB
def build_vector_db():
    docs = load_documents("rag_docs")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="llama3")  # or mistral
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="chroma_db")
    vectordb.persist()
    return vectordb

# 3. RAG pipeline
def get_qa_chain():
    vectordb = Chroma(persist_directory="chroma_db", embedding_function=OllamaEmbeddings(model="llama3"))
    retriever = vectordb.as_retriever()
    llm = Ollama(model="llama3")  # or mistral
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain

# 4. Chat endpoint
qa_chain = get_qa_chain()

def ask_chatbot(query: str):
    return qa_chain.run(query)
