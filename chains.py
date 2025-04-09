from langchain.chains import create_histore_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from memory import get_session_hystory
from prompts import contextualize_prompt, qa_prompt
from settings import OPENAI_MODEL, OPENAI_TEMPERATURE
from vectorstore import get_vectorstore


def get_rag_chain() -> RunnableWithMessageHistory:
    """
    Create a chain that retrieves relevant documents from a vector store and generates a response using an LLM.
    The chain consists of two main components:
    1. A retriever that fetches relevant documents based on the user's query.
    2. A question-answering chain that processes the retrieved documents and generates a response.
    """
    # Create a retriever from the vector store
    retriever = get_vectorstore().as_retriever()
    llm = ChatOpenAI(model_name=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE)
    history_aware_chain = create_histore_aware_retriever(
        llm, retriever, contextualize_prompt
    )
    question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)
    return create_retrieval_chain(history_aware_chain, question_answer_chain)


def get_conversational_rag_chain():
    """
    Create a conversational chain that retrieves relevant documents and generates a response using an LLM.
    This chain is designed to maintain a conversation history and provide context-aware responses.
    """
    # Create a retriever from the vector store
    rag_chain = get_rag_chain()
    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_hystory,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
