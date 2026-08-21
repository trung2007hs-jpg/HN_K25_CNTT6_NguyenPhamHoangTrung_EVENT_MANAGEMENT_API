from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

