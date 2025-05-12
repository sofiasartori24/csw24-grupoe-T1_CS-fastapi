from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.curriculum import curriculum_discipline_association

class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    program = Column(Text, nullable=False)
    bibliography = Column(Text, nullable=False)

    classes = relationship("Class", back_populates="discipline")
    lessons = relationship("Lesson", back_populates="discipline")
    # Many-to-Many relationship with Curriculum
    curriculums = relationship(
        "Curriculum",
        secondary=curriculum_discipline_association,
        back_populates="disciplines",
    )