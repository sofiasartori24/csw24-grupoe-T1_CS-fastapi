from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    statement = Column(String, nullable=False)
    type = Column(String, nullable=False)

    # Relationships
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    class_instance = relationship("Class", back_populates="evaluations")