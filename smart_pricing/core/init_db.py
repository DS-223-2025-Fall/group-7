from config import create_engine_from_env
from models import Base

def main():
    engine = create_engine_from_env(echo=True)
    Base.metadata.create_all(engine)
    print("Database tables successfully created.")

if name == "__main__":
    main()