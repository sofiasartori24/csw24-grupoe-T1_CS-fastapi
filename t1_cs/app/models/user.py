from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(255), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", back_populates="users")
    classes_taught = relationship("Class", back_populates="professor")