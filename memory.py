from langchain_community.chat_message_histories import RedisChatMessageHistory

from settings import REDIS_URL

def get_session_hystory(session_id: str) -> RedisChatMessageHistory:
    """
    Create a Redis chat message history instance for a given session ID.
    This allows for storing and retrieving chat messages in a Redis database.
    """
    return RedisChatMessageHistory(
        url=REDIS_URL,
        session_id=session_id,
        ttl=3600,  # Set the time-to-live for the session history to 1 hour
    )
