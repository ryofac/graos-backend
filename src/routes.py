import time

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from config import get_settings
from infra import get_db
from models import TemperatureReading
from schemas import TemperatureResponseSchema
from utils.telegram_utils import send_telegram_alert

settings = get_settings()
temp_router = APIRouter(prefix="", tags=["monitor"])


# Variável global para armazenar o timestamp do último alerta
last_alert_time = 0


@temp_router.get("/temp")
async def get_temperature(
    gas_level: float = Query(..., description="Nível de gás a ser registrado"),
    temperature: float = Query(..., description="Temperatura a ser registrada"),
    moisture: float = Query(..., description="Nível de Umidade a ser registrada"),
    sensor_id: int = Query(..., description="ID do sensor"),
    db: Session = Depends(get_db),
) -> TemperatureResponseSchema:
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

    if (
        temperature < settings.temperature_interval[0]
        or temperature > settings.temperature_interval[1]
    ):
        alert_message += (
            f"⚠️🔥 *ALERTA DE TEMPERATURA!* 🔥⚠️\n"
            f"A temperatura está em *{temperature}°C*, fora do *intervalo ideal* ({settings.temperature_interval[0]}°C e {settings.temperature_interval[1]}°C)\n\n"
        )

    if (
        moisture < settings.moisture_interval[0]
        or moisture > settings.moisture_interval[1]
    ):
        alert_message += (
            f"⚠️💧 *ALERTA DE UMIDADE!* 💧⚠️\n"
            f"A umidade está em *{moisture}%*, fora do *intervalo ideal* ({settings.moisture_interval[0]}% e {settings.moisture_interval[1]}%)*\n\n"
        )

    if gas_level < settings.gas_level_interval[0] or settings.gas_level_interval[1]:
        alert_message += (
            f"⚠️🛢️ *ALERTA DE GÁS!* 🛢️⚠️\n"
            f"O nível de gás está em *{gas_level}%*, fora do *intervalo ideal* ({settings.moisture_interval[0]}% e {settings.moisture_interval[1]}%)*!\n\n"
        )

    # Verifica se passaram pelo menos 10 segundos desde o último alerta
    current_time = time.time()
    global last_alert_time
    if alert_message and (current_time - last_alert_time) > 10:
        alert_message += f"\nConvido você a ver as mudanças em tempo real, por {settings.dashboard_link}"
        send_telegram_alert(
            alert_message, settings.telegram_bot_token, settings.telegram_chat_id
        )
        last_alert_time = current_time

    return TemperatureResponseSchema(
        message="Dados recebidos",
        sensor_id=sensor_id,
        gas_level=gas_level,
        moisture=moisture,
        temperature=temperature,
    )
