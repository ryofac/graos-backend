from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

DATABASE_URL = settings.database_url
if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
