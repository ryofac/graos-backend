from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from infra import get_db
from models import TemperatureReading
from telegram_utils import send_telegram_alert

app = FastAPI(docs_url="/docs", on_startup=[])


MAX_TEMPERATURE = 30.0  # Valor máximo para temperatura
MAX_MOISTURE = 80.0  # Valor máximo para umidade
MAX_GAS_LEVEL = 1.0  # Valor máximo para nível de gás

# Variáveis de configuração do bot do Telegram
TELEGRAM_BOT_TOKEN = "8125401548:AAFPwRl5P2fl9sCM7XzqWUkUqBOMCHZY-FU"
TELEGRAM_CHAT_ID = "984362796"


@app.get("/temp")
async def get_temperature(
    gas_level: float = Query(..., description="Nível de gás a ser registrado"),
    temperature: float = Query(..., description="Temperatura a ser registrada"),
    moisture: float = Query(..., description="Nível de Umidade a ser registrada"),
    sensor_id: int = Query(..., description="ID do sensor"),
    db: Session = Depends(get_db),
):
    new_reading = TemperatureReading(
        sensor_id=sensor_id,
        temperature=temperature,
        moisture=moisture,
        gas_level=gas_level,
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    alert_message = ""

    if temperature > MAX_TEMPERATURE:
        alert_message += f"Atenção! Temperatura ({temperature}°C) excedeu o limite de {MAX_TEMPERATURE}°C.\n"

    if moisture > MAX_MOISTURE:
        alert_message += (
            f"Atenção! Umidade ({moisture}%) excedeu o limite de {MAX_MOISTURE}%.\n"
        )

    if gas_level > MAX_GAS_LEVEL:
        alert_message += f"Atenção! Nível de gás ({gas_level}%) excedeu o limite de {MAX_GAS_LEVEL}%.\n"

    # Se houver alerta, envia para o Telegram
    if alert_message:
        send_telegram_alert(alert_message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    response = {
        "message": "Dados recebidos",
        "temperature": temperature,
        "sensor_id": sensor_id,
        "gas_level": gas_level,
        "moisture": moisture,
    }
    print(response)
    return response
