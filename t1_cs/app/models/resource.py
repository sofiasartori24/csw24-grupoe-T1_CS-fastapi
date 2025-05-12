from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class ResourceStatus(str, enum.Enum):
    available = "available"
    maintenance = "maintenance"
    taken = "taken"

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.available, nullable=False)

    # Relationships
    resource_type_id = Column(Integer, ForeignKey("resource_types.id"), nullable=False)
    resource_type = relationship("ResourceType", back_populates="resources")
    reservations = relationship("Reservation", back_populates="resource")

    rooms = relationship(
        "Room",
        secondary="room_resource",
        back_populates="resources",
    )