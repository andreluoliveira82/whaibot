from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from core.memory import get_session_history
from core.prompts import contextualize_prompt, qa_prompt
# from settings import OPENAI_MODEL_NAME, OPENAI_MODEL_TEMPERATURE
from core.settings import GROQ_MODEL_NAME, GROQ_API_KEY, MODEL_TEMPERATURE
from core.vectorstore import get_vectorstore


def get_rag_chain():
    """
    Create a chain that retrieves relevant documents from a vector store and generates a response using an LLM.
    The chain consists of two main components:
    1. A retriever that fetches relevant documents based on the user's query.
    2. A question-answering chain that processes the retrieved documents and generates a response.
    """
    # Create a retriever from the vector store
    # llm = ChatOpenAI(model=OPENAI_MODEL_NAME, temperature=MODEL_TEMPERATURE)
    llm = ChatGroq(model=GROQ_MODEL_NAME,  groq_api_key=GROQ_API_KEY,temperature=MODEL_TEMPERATURE)
    retriever = get_vectorstore().as_retriever()
    history_aware_chain = create_history_aware_retriever(
        llm, retriever, contextualize_prompt
    )
    question_answer_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt,
    )
    return create_retrieval_chain(history_aware_chain, question_answer_chain)


def get_conversational_rag_chain():
    """
    Create a conversational chain that retrieves relevant documents and generates a response using an LLM.
    This chain is designed to maintain a conversation history and provide context-aware responses.
    """

    rag_chain = get_rag_chain()

    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
