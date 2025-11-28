import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = None   

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_database_url():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")

    host = os.getenv("DB_HOST")
    if not host or host == "localhost":
        host = os.getenv("DB_SERVICE_NAME", "db")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

def create_engine_from_env(echo=False):
    global engine
    if engine is None:
        url = get_database_url()
        engine = create_engine(url, echo=echo)
        SessionLocal.configure(bind=engine)
    return engine
