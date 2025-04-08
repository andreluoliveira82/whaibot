import requests
from settings import (
    EVOLUTION_API_URL,
    EVOLUTION_INSTANCE_NAME,
    EVOLUTION_AUTHENTICATION_API_KEY,
)


def send_whatsapp_message(phone_number: str, message: str) -> dict:
    """
    Send a whatsapp message to a phone number
    :param phone_number: The phone number to send the message to (in the format '5511999999999')
    :param message: The message to send
    :return: A dictionary with the status of the request
    """
    if not phone_number or not message:
        return {
            "status": "error",
            "error": "Número de telefone ou mensagem não podem ser vazios.",
        }

    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}"
    headers = {
        "apikey": EVOLUTION_AUTHENTICATION_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "number": phone_number,
        "text": message,
    }

    try:
        response = requests.post(url=url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")
        return {"status": "error", "error": str(e)}

    return {"status": "success", "message": "Mensagem enviada"}
