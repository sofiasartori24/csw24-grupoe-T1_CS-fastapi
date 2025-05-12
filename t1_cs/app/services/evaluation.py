from sqlalchemy.orm import Session
from app.repositories.evaluation import EvaluationRepository
from app.schemas.evaluation import EvaluationCreate

class EvaluationService:
    @staticmethod
    def get_all_evaluations(db: Session):
        return EvaluationRepository.get_all(db)

    @staticmethod
    def get_evaluation_by_id(db: Session, evaluation_id: int):
        return EvaluationRepository.get_by_id(db, evaluation_id)

    @staticmethod
    def create_evaluation(db: Session, evaluation: EvaluationCreate):
        return EvaluationRepository.create(db, evaluation)