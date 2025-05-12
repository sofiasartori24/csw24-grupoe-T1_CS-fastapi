from sqlalchemy.orm import Session
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate

class EvaluationRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Evaluation).all()

    @staticmethod
    def get_by_id(db: Session, evaluation_id: int):
        return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    @staticmethod
    def create(db: Session, evaluation: EvaluationCreate):
        db_evaluation = Evaluation(
            date=evaluation.date,
            statement=evaluation.statement,
            type=evaluation.type,
            class_id=evaluation.class_id,
        )
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)
        return db_evaluation