"""
Database configuration module.

This module handles loading environment variables, constructing the database
URL, and creating the SQLAlchemy engine and session used across the project.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = None   

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def get_database_url():
    """
    Constructs the database URL from environment variables.

    Returns:
        str: A full SQLAlchemy-compatible database connection URL.

    Notes:
        - DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, DB_HOST are expected in .env
        - If DB_HOST is missing or 'localhost', DB_SERVICE_NAME is used.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")

    host = os.getenv("DB_HOST")
    if not host or host == "localhost":
        host = os.getenv("DB_SERVICE_NAME", "db")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

def create_engine_from_env(echo=False):
    """
    Creates a SQLAlchemy engine using environment variables and configure SessionLocal.

    Args:
         echo (bool): If True, SQL queries will be logged to the console.

    Returns:
        Engine: A SQLAlchemy Engine instance connected to the configured database.

    Notes:
        - The engine is created only once.
        - SessionLocal is automatically bound to the created engine.
    """
    global engine
    if engine is None:
        url = get_database_url()
        engine = create_engine(url, echo=echo)
        SessionLocal.configure(bind=engine)
    return engine
