from sqlalchemy.orm import Session
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate

class EvaluationRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Evaluation).all()

    def get_by_id(self, db: Session, evaluation_id: int):
        return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    def create(self, db: Session, evaluation: EvaluationCreate):
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

    def update(self, db: Session, evaluation_id: int, evaluation_update: EvaluationUpdate):
        db_evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if db_evaluation:
            for field, value in evaluation_update.dict(exclude_unset=True).items():
                setattr(db_evaluation, field, value)
            db.commit()
            db.refresh(db_evaluation)
        return db_evaluation

    def delete(self, db: Session, evaluation_id: int):
        db_evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if db_evaluation:
            db.delete(db_evaluation)
            db.commit()
        return db_evaluation
