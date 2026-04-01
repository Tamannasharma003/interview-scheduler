import os
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 

# ✅ Use DATABASE_URL
MYSQL_URL = os.getenv("MYSQL_URL") 

if not MYSQL_URL: 
    raise ValueError("❌ MYSQL_URL not found in environment variables") 

# ✅ Fix driver
if MYSQL_URL.startswith("mysql://"): 
    MYSQL_URL = MYSQL_URL.replace("mysql://", "mysql+pymysql://") 

# ✅ Create engine 
engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True
) 

# ✅ Session 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base 
Base = declarative_base()


# ✅ 🔥 THIS WAS MISSING
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
