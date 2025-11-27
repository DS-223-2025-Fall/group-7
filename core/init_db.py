"""
Database initialization script.

Creates all database tables defined in the SQLAlchemy models.
"""

from config import create_engine_from_env
from models import Base

def main():
    """
    Create database tables using the engine from environment settings.
    """
    engine = create_engine_from_env(echo=True)
    Base.metadata.create_all(engine)
    print("Database tables successfully created.")

if __name__ == "__main__":
    main()
