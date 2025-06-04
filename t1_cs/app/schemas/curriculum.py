from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List
from app.schemas.discipline import DisciplineResponse

class CurriculumBase(BaseModel):
    course_name: str
    start_date: date
    end_date: Optional[date] = None

class CurriculumCreate(CurriculumBase):
    discipline_ids: List[int]

class CurriculumUpdate(CurriculumBase):
    discipline_ids: Optional[List[int]] = None

class CurriculumResponse(CurriculumBase):
    id: int
    disciplines: List[DisciplineResponse]

    model_config = ConfigDict(from_attributes=True)
