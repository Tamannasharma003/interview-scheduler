from fastapi import FastAPI
from .database import engine
from .model import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Interview Scheduler Backend Running"}
from sqlalchemy.orm import Session
from .database import SessionLocal
from .model import Interview


@app.post("/schedule-interview")
def schedule_interview(manager_id: int, candidate_id: int, time_slot: str):

    db = SessionLocal()

    interview = Interview(
        manager_id=manager_id,
        candidate_id=candidate_id,
        slot=time_slot
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return {
        "message": "Interview scheduled",
        "interview_id": interview.id
    }

