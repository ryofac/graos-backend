from fastapi import FastAPI

from config import get_settings
from routes import temp_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    docs_url="/docs",
    on_startup=[],
)
app.include_router(temp_router)
