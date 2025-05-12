from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    semester = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    vacancies = Column(Integer, nullable=False)

    # Relationships
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    discipline = relationship("Discipline", back_populates="classes")
    professor = relationship("User", back_populates="classes_taught")
    evaluations = relationship("Evaluation", back_populates="class_instance")
    lessons = relationship("Lesson", back_populates="class_instance")