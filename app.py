from fastapi import FastAPI, Request

from evolution_api import send_whatsapp_message


app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request) -> dict:
    """
    Webhook endpoint to receive messages from WhatsApp. The webhook is triggered when a message is received.
    The webhook processes the incoming message and sends a reply back to the sender.
    """
    data = await request.json()
    chat_id = data.get("data").get("key").get("remoteJid")
    received_message = data.get("data").get("message").get("conversation")

    # check if chat_id and message are not None
    # and chat_id does not contain '@g.us' (group chat)
    if chat_id and received_message and "@g.us" not in chat_id:
        send_whatsapp_message(
            phone_number=chat_id,
            message=f"Opa, tudo bem mano?\nVocê me mandou a seguir mensagem:\n{received_message}"
        )

    return {"status": "success", "message": "Message processed"}
