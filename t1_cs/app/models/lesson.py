from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    attendance = Column(String, nullable=True)  

    # Relationships
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), nullable=False)

    class_instance = relationship("Class", back_populates="lessons")
    room = relationship("Room", back_populates="lessons")
    discipline = relationship("Discipline", back_populates="lessons")
    reservations = relationship("Reservation", back_populates="lesson")