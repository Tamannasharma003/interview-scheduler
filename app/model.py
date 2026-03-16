from sqlalchemy import Column, Integer, String
from .database import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer)
    candidate_id = Column(Integer)
    slot = Column(String(50))
    status = Column(String(50))


  