from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    building_number = Column(Integer, nullable=False, unique=True)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    complement = Column(String, nullable=True)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    # Relationship with Room
    rooms = relationship("Room", back_populates="building")