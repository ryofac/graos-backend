import requests
from fastapi import HTTPException


# Função para enviar o alerta para o Telegram
def send_telegram_alert(message: str, bot_token: str, chat_id: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Erro ao enviar mensagem para o Telegram"
        )
