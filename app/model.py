from sqlalchemy import Column, Integer, String
from database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    manager_name = Column(String)
    candidate_name = Column(String)
    time_slot = Column(String)
    selected_slot = Column(String)
    status = Column(String)
