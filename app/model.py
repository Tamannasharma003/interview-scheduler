from sqlalchemy import Column, Integer, String, Text
from database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(String(20), nullable=True)
    candidate_id = Column(String(20), nullable=True)
    slots = Column(Text, nullable=True)
    selected_slot = Column(String(255), nullable=True)
    status = Column(String(20), default="pending")
