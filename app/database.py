import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Get DB URL from Railway
MYSQL_URL = os.getenv("MYSQL_URL")

if not MYSQL_URL:
    raise ValueError("❌ MYSQL_URL not found in environment variables")

# ✅ Fix driver
if MYSQL_URL.startswith("mysql://"):
    MYSQL_URL = MYSQL_URL.replace("mysql://", "mysql+pymysql://")

# ✅ Create engine
engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True,
    pool_recycle=280
)

# ✅ Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base
Base = declarative_base()


# ✅ 🔥 ADD THIS FUNCTION HERE (IMPORTANT)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
