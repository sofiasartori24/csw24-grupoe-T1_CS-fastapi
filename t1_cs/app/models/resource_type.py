from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class ResourceType(Base):
    __tablename__ = "resource_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    # Relationship with Resource
    resources = relationship("Resource", back_populates="resource_type")