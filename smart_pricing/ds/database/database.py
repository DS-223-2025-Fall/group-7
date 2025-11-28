import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_url():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "5432")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(get_db_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
