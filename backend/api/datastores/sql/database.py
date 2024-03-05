from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.config import config

SQLALCHEMY_DATABASE_URL = config["datastores"]["sqlalchemy"]["database_url"]


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database connection, used as a dependency inhjection.
def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
