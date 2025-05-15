from sqlalchemy.orm import Session
from app.repositories.evaluation import EvaluationRepository
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate
from fastapi import HTTPException

class EvaluationService:
    def __init__(self):
        self.repository = EvaluationRepository()

    def get_all_evaluations(self, db: Session):
        return self.repository.get_all(db)

    def get_evaluation_by_id(self, db: Session, evaluation_id: int):
        evaluation = self.repository.get_by_id(db, evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return evaluation

    def create_evaluation(self, db: Session, evaluation: EvaluationCreate):
        return self.repository.create(db, evaluation)

    def update_evaluation(self, db: Session, evaluation_id: int, evaluation_update: EvaluationUpdate):
        evaluation = self.repository.update(db, evaluation_id, evaluation_update)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return evaluation

    def delete_evaluation(self, db: Session, evaluation_id: int):
        evaluation = self.repository.delete(db, evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return {"message": "Evaluation deleted successfully"}
