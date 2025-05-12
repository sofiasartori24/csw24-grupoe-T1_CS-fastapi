from sqlalchemy.orm import Session
from app.models.curriculum import Curriculum
from app.models.discipline import Discipline
from app.schemas.curriculum import CurriculumCreate

class CurriculumRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Curriculum).all()

    @staticmethod
    def get_by_id(db: Session, curriculum_id: int):
        return db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()

    @staticmethod
    def create(db: Session, curriculum: CurriculumCreate):
        db_curriculum = Curriculum(
            course_name=curriculum.course_name,
            start_date=curriculum.start_date,
            end_date=curriculum.end_date,
        )
        # Associate disciplines
        disciplines = db.query(Discipline).filter(Discipline.id.in_(curriculum.discipline_ids)).all()
        db_curriculum.disciplines = disciplines

        db.add(db_curriculum)
        db.commit()
        db.refresh(db_curriculum)
        return db_curriculum

    @staticmethod
    def delete(db: Session, curriculum_id: int):
        db_curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        if db_curriculum:
            db.delete(db_curriculum)
            db.commit()
        return db_curriculum