import environs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

env = environs.Env()

class Database:

    def __init__(self):
        engine = create_engine(env('DATABASE_URI'))
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.engine = engine
        self.conn = engine.connect()