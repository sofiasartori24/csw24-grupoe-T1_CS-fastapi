from pydantic import BaseModel, ConfigDict
from datetime import date
from app.schemas.discipline import DisciplineResponse

class CurriculumBase(BaseModel):
    course_name: str
    start_date: date
    end_date: date | None = None

class CurriculumCreate(CurriculumBase):
    discipline_ids: list[int]  # List of discipline IDs to associate

class CurriculumResponse(CurriculumBase):
    id: int
    disciplines: list[DisciplineResponse]  # List of associated disciplines

    model_config = ConfigDict(from_attributes=True)