import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Get Railway MySQL URL
DATABASE_URL = os.getenv("MYSQL_URL")

if not DATABASE_URL:
    raise ValueError("❌ MYSQL_URL not found in environment variables")

# ✅ Fix mysql driver
DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

# ✅ Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# ✅ Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base
Base = declarative_base()
