from pydantic import BaseModel, ConfigDict
from datetime import date
from app.schemas.discipline import DisciplineResponse

class CurriculumBase(BaseModel):
    course_name: str
    start_date: date
    end_date: date | None = None

class CurriculumCreate(CurriculumBase):
    discipline_ids: list[int]  

class CurriculumUpdate(CurriculumBase):
    discipline_ids: list[int] | None = None  

class CurriculumResponse(CurriculumBase):
    id: int
    disciplines: list[DisciplineResponse]  

    model_config = ConfigDict(from_attributes=True)
