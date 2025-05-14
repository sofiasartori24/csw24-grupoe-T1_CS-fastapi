from sqlalchemy.orm import Session
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate

class EvaluationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Evaluation).all()

    def get_by_id(self, evaluation_id: int):
        return self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    def create(self, evaluation: EvaluationCreate):
        db_evaluation = Evaluation(
            date=evaluation.date,
            statement=evaluation.statement,
            type=evaluation.type,
            class_id=evaluation.class_id,
        )
        self.db.add(db_evaluation)
        self.db.commit()
        self.db.refresh(db_evaluation)
        return db_evaluation

    def update(self, evaluation_id: int, evaluation_update: EvaluationUpdate):
        db_evaluation = self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if db_evaluation:
            for field, value in evaluation_update.dict(exclude_unset=True).items():
                setattr(db_evaluation, field, value)
            self.db.commit()
            self.db.refresh(db_evaluation)
        return db_evaluation

    def delete(self, evaluation_id: int):
        db_evaluation = self.db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
        if db_evaluation:
            self.db.delete(db_evaluation)
            self.db.commit()
        return db_evaluation
