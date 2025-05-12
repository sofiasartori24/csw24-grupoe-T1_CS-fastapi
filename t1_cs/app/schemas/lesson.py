from pydantic import BaseModel, ConfigDict
from datetime import date
from app.schemas.class_schema import ClassResponse
from app.schemas.room import RoomResponse
from app.schemas.discipline import DisciplineResponse

class LessonBase(BaseModel):
    date: date
    attendance: str | None = None

class LessonCreate(LessonBase):
    class_id: int
    room_id: int
    discipline_id: int

class LessonResponse(LessonBase):
    id: int
    class_instance: ClassResponse
    room: RoomResponse
    discipline: DisciplineResponse

    model_config = ConfigDict(from_attributes=True)