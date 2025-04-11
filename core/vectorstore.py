import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings

from core.settings import VECTOR_STORE_PATH, RAG_FILES_DIR


def load_documents() -> list:
    """
    Load documents from the specified directory.

    Args:
        rag_files_dir (str): Directory containing the documents.

    Returns:
        list: List of loaded documents.
    """
    documents = []

    os.makedirs(RAG_FILES_DIR, exist_ok=True)
    processed_dir = os.path.join(RAG_FILES_DIR, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    files = [
        os.path.join(RAG_FILES_DIR, f)
        for f in os.listdir(RAG_FILES_DIR)
        if f.endswith((".pdf", ".txt"))
    ]

    for file in files:
        try:
            loader = PyPDFLoader(file) if file.endswith(".pdf") else TextLoader(file)
            documents.extend(loader.load())

            # Move o arquivo processado
            dest_path = os.path.join(processed_dir, os.path.basename(file))
            shutil.move(file, dest_path)
        except Exception as e:
            print(f"Erro ao processar {file}: {str(e)}")

    return documents


def get_vectorstore() -> Chroma:
    # usando o embeddings do groq AI
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # Verifica se há novos arquivos para processar
    has_new_files = any(f.endswith((".pdf", ".txt")) for f in os.listdir(RAG_FILES_DIR))

    if os.path.exists(VECTOR_STORE_PATH) and not has_new_files:
        return Chroma(
            persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings
        )

    # Força recriação se houver novos arquivos
    shutil.rmtree(VECTOR_STORE_PATH, ignore_errors=True)

    # Cria o vetorstore
    documents = load_documents()

    if documents:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)

        return Chroma.from_documents(
            texts, embeddings, persist_directory=VECTOR_STORE_PATH
        )

    return Chroma.from_documents(texts, embeddings, persist_directory=VECTOR_STORE_PATH)
