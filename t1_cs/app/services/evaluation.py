from sqlalchemy.orm import Session
from app.repositories.evaluation import EvaluationRepository
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate
from fastapi import HTTPException

class EvaluationService:
    def __init__(self, db: Session):
        self.repository = EvaluationRepository(db)

    def get_all_evaluations(self):
        return self.repository.get_all()

    def get_evaluation_by_id(self, evaluation_id: int):
        evaluation = self.repository.get_by_id(evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return evaluation

    def create_evaluation(self, evaluation: EvaluationCreate):
        return self.repository.create(evaluation)

    def update_evaluation(self, evaluation_id: int, evaluation_update: EvaluationUpdate):
        evaluation = self.repository.update(evaluation_id, evaluation_update)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return evaluation

    def delete_evaluation(self, evaluation_id: int):
        evaluation = self.repository.delete(evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return {"message": "Evaluation deleted successfully"}
