import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

print("👉 DATABASE_URL:", DATABASE_URL)  # DEBUG LINE

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in environment variables")

DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
