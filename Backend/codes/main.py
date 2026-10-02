from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from codes.database import engine, get_db
from codes.models import Base, Customer, Complaint

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ComplaintCreate(BaseModel):
    customer_name: str
    message: str
    issue_type: str


@app.get("/")
def read_root():
    return {"message": "Prudence backend is running"}


@app.post("/complaints")
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    new_complaint = Complaint(
        customer_name=complaint.customer_name,
        message=complaint.message,
        issue_type=complaint.issue_type,
        status="received",
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


@app.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).all()

    return complaints
