from langchain_community.chat_message_histories import RedisChatMessageHistory

from core.settings import REDIS_URL

def get_session_history(session_id: str):
    """
    Create a Redis chat message history instance for a given session ID.
    This allows for storing and retrieving chat messages in a Redis database.
    """
    return RedisChatMessageHistory(
        url=REDIS_URL,
        session_id=session_id,
    )
