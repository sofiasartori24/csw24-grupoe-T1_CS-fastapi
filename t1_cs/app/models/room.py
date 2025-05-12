from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for the many-to-many relationship between Room and Resource
room_resource_association = Table(
    "room_resource",
    Base.metadata,
    Column("room_id", Integer, ForeignKey("rooms.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id"), primary_key=True),
)

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    floor = Column(String, nullable=False)

    # Relationships
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    building = relationship("Building", back_populates="rooms")
    lessons = relationship("Lesson", back_populates="room")
    resources = relationship(
        "Resource",
        secondary=room_resource_association,
        back_populates="rooms",
    )