from sqlalchemy import Column, Integer, String
from database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    manager = Column(String(50))
    slots = Column(String(255))
    selected_slot = Column(String(50))
    status = Column(String(20))
