from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  
    building_number = Column(Integer, nullable=False, unique=True)
    street = Column(String(255), nullable=False)
    number = Column(String(50), nullable=False) 
    complement = Column(String(100), nullable=True)  
    neighborhood = Column(String(100), nullable=False)  
    city = Column(String(100), nullable=False) 
    state = Column(String(2), nullable=False)  
    postal_code = Column(String(10), nullable=False)  

    rooms = relationship("Room", back_populates="building")
