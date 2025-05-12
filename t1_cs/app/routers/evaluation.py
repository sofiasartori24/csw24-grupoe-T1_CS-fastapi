from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.evaluation import EvaluationService
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EvaluationResponse)
def create_evaluation(evaluation: EvaluationCreate, db: Session = Depends(get_db)):
    return EvaluationService.create_evaluation(db, evaluation)