from core import create_engine_from_env, Base

def main():
    engine = create_engine_from_env(echo=True)
    Base.metadata.create_all(bind=engine)
    print("Database tables created")


if __name__ == "__main__":
    main()
