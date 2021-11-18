from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# USER = "nspdsyefuxriqm"
# PASSWORD = "1532f0eea628e84e3bddf102e09920722e0f7f5020a3224350f0d2d533bae05a"
# HOST = "ec2-44-199-40-188.compute-1.amazonaws.com"
# DATABASE = "dfiumv6bioofku"

USER = "postgres"
PASSWORD = "bgs280901"
HOST = "localhost"
DATABASE = "test1rpl"

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()