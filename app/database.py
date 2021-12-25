from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))    
DB_USERNAME = os.getenv('DATABASE_USER') 
DB_PASSWORD = os.getenv('DATABASE_PSW')

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5435/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()