from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for the many-to-many relationship between Curriculum and Discipline
curriculum_discipline_association = Table(
    "curriculum_discipline",
    Base.metadata,
    Column("curriculum_id", Integer, ForeignKey("curriculums.id"), primary_key=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id"), primary_key=True),
)

class Curriculum(Base):
    __tablename__ = "curriculums"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Many-to-Many relationship with Discipline
    disciplines = relationship(
        "Discipline",
        secondary=curriculum_discipline_association,
        back_populates="curriculums",
    )