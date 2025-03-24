from pydantic import BaseModel


class TemperatureResponseSchema(BaseModel):
    message: str
    sensor_id: int
    moisture: float
    gas_level: float
    temperature: float
