from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HostIp = os.getenv("HOST")
DB = os.getenv("DB")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HostIp}/{DB}"
print("Connecting to DB:", DATABASE_URL)

con_factory = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=con_factory)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
