import os
import shutil
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from settings import VECTOR_STORE_PATH, RAG_FILES_DIR


def load_documents() -> list:
    """
    Load documents from the specified directory.

    Args:
        rag_files_dir (str): Directory containing the documents.

    Returns:
        list: List of loaded documents.
    """
    documents = []
    processed_dir = os.path.join(RAG_FILES_DIR, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith(".pdf") or f.endswith(".txt")
    ]
    for file in files:
        loader = PyMuPDFLoader(file) if file.endswith(".pdf") else TextLoader(file)
        documents.extend(loader.load())

        # Move the processed file to the processed directory
        dest_path = os.path.join(processed_dir, os.path.basename(file))
        shutil.move(file, dest_path)

    return documents

def get_vectorstore() -> Chroma:
    """
    Get the vector store for the documents.

    Returns:
        Chroma: The vector store instance.
    """
    if os.path.exists(VECTOR_STORE_PATH):
        return Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=OpenAIEmbeddings())

    documents = load_documents()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(texts, embeddings, persist_directory=VECTOR_STORE_PATH)
    vectorstore.persist()

    return vectorstore
