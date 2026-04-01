from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime


# =========================
# 🔹 JOBS TABLE
# =========================
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    role = Column(String(255))


# =========================
# 🔹 CANDIDATES TABLE
# =========================
class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(String(20), primary_key=True)
    name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    job_id = Column(Integer, ForeignKey("jobs.id"))


# =========================
# 🔹 MANAGERS TABLE
# =========================
class Manager(Base):
    __tablename__ = "managers"

    manager_id = Column(String(20), primary_key=True)
    name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    job_id = Column(Integer, ForeignKey("jobs.id"))


# =========================
# 🔹 INTERVIEWS TABLE
# =========================
class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True)

    manager_id = Column(String(20), ForeignKey("managers.manager_id"))
    candidate_id = Column(String(20), ForeignKey("candidates.candidate_id"))

    job_id = Column(Integer, ForeignKey("jobs.id"))

    manager_slots = Column(Text)
    selected_slot = Column(DateTime)

    status = Column(String(50), default="pending")

    job_role = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
