from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from infra import get_db
from models import TemperatureReading

app = FastAPI(docs_url="/docs", on_startup=[])


@app.get("/temp")
async def get_temperature(
    ruid: float = Query(..., description="Nível de ruído a ser registrado"),
    temperature: float = Query(..., description="Temperatura a ser registrada"),
    sensor_id: int = Query(..., description="ID do sensor"),
    db: Session = Depends(get_db),
):
    new_reading = TemperatureReading(
        sensor_id=sensor_id, temperature=temperature, ruid=ruid
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    response = {
        "message": "Dados recebidos",
        "temperature": temperature,
        "sensor_id": sensor_id,
        "ruid": ruid,
    }
    print(response)
    return response
