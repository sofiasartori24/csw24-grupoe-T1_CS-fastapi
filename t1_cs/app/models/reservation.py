from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    observation = Column(String(255), nullable=True)

    # Relationships
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    lesson = relationship("Lesson", back_populates="reservations")
    resource = relationship("Resource", back_populates="reservations")