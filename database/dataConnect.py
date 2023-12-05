from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://hetbabariya:het9676@localhost/fastapi_verification"

engin = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engin , autoflush=False , autocommit = False)

base = declarative_base()