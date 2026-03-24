from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    manager_id = Column(Integer)
    candidate_id = Column(Integer)

    slots = Column(String(255))          # manager slots
    selected_slot = Column(String(50))   # candidate choice
    status = Column(String(20))          # pending / confirmed
