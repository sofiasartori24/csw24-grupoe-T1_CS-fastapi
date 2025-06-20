from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.lesson import LessonResponse
from app.schemas.resource import ResourceResponse

class ReservationBase(BaseModel):
    observation: Optional[str] = None

class ReservationCreate(ReservationBase):
    lesson_id: int
    resource_id: int

class ReservationResponse(ReservationBase):
    id: int
    lesson: LessonResponse
    resource: ResourceResponse

    model_config = ConfigDict(from_attributes=True)