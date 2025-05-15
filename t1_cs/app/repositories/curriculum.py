from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum
from app.models.discipline import Discipline
from app.schemas.curriculum import CurriculumCreate, CurriculumUpdate
from fastapi import HTTPException

class CurriculumRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Curriculum).all()

    def get_by_id(self, db: Session, curriculum_id: int):
        return db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()

    def create(self, db: Session, curriculum: CurriculumCreate):
        # Create new Curriculum
        db_curriculum = Curriculum(
            course_name=curriculum.course_name,
            start_date=curriculum.start_date,
            end_date=curriculum.end_date,
        )
        # Associate disciplines
        disciplines = self.db.query(Discipline).filter(Discipline.id.in_(curriculum.discipline_ids)).all()
        db_curriculum.disciplines = disciplines

        db.add(db_curriculum)
        db.commit()
        db.refresh(db_curriculum)
        return db_curriculum

    def update(self, db: Session, curriculum_id: int, curriculum_update: CurriculumUpdate):
        db_curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        if not db_curriculum:
            return None
        # Update the fields
        if curriculum_update.course_name:
            db_curriculum.course_name = curriculum_update.course_name
        if curriculum_update.start_date:
            db_curriculum.start_date = curriculum_update.start_date
        if curriculum_update.end_date:
            db_curriculum.end_date = curriculum_update.end_date

        if curriculum_update.discipline_ids is not None:
            # Associate new disciplines
            disciplines = self.db.query(Discipline).filter(Discipline.id.in_(curriculum_update.discipline_ids)).all()
            db_curriculum.disciplines = disciplines

        db.commit()
        db.refresh(db_curriculum)
        return db_curriculum

    def delete(self, db: Session, curriculum_id: int):
        db_curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        if db_curriculum:
            db.delete(db_curriculum)
            db.commit()
        return db_curriculum
