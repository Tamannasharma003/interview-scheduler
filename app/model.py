from sqlalchemy import Column, Integer, String
from database import Base   # 👈 your db file name

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    manager = Column(String)
    candidate = Column(String)
    slots = Column(String)
    selected_slot = Column(String)
    status = Column(String)
