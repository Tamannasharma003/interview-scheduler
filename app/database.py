import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Get Railway MySQL URL
DATABASE_URL = os.getenv("mysql://root:wWDHfdlCwFOjiytrgZLXfCcwMwvHjOnr@mysql.railway.internal:3306/railway")

if not DATABASE_URL:
    raise ValueError("❌ MYSQL_URL not found in environment variables")

# ✅ Fix mysql driver
DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

# ✅ Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
