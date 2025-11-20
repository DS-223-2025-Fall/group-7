from db.models import Base
from utils.config import create_engine_from_env

def init_db(echo=True):
    engine = create_engine_from_env(echo=echo)
    Base.metadata.create_all(engine)
