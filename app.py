from fastapi import FastAPI, Request

from chains import get_conversational_rag_chain
from evolution_api import send_whatsapp_message


app = FastAPI()

conversational_rag_chain = get_conversational_rag_chain()


@app.post("/webhook")
async def webhook(request: Request) -> dict:
    """
    Webhook endpoint to receive messages from WhatsApp. The webhook is triggered when a message is received.
    The webhook processes the incoming message and sends a reply back to the sender.
    """
    data = await request.json()
    chat_id = data.get("data").get("key").get("remoteJid")
    received_message = data.get("data").get("message").get("conversation")

    # ignore self messages (messages sent from me)
    if data.get("data").get("key").get("fromMe"):
        return {"status": "ignored", "message": "Self message ignored"}

    # check if chat_id and message are not None
    # and chat_id does not contain '@g.us' (group chat)
    if chat_id and received_message and "@g.us" not in chat_id:
        ai_response = conversational_rag_chain.invoke(
            input={"input": received_message},
            config={"configurable": {"session_id": chat_id}},
        )["answer"]

        # Send the AI response back to the user on WhatsApp
        send_whatsapp_message(phone_number=chat_id, message=ai_response)

    return {"status": "success", "message": "Message processed"}
