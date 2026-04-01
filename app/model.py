from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db import Base

# 🔹 JOB TABLE
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(255))
  



# 🔹 INTERVIEW TABLE
class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    manager_id = Column(String(20))
    candidate_id = Column(String(20))

    job_id = Column(Integer, ForeignKey("jobs.id"))  # ✅ NEW

    manager_slots = Column(Text)
    selected_slot = Column(DateTime)

    status = Column(String(20), default="pending")
