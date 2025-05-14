from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.discipline import DisciplineResponse
from app.schemas.user import UserResponse
from app.schemas.evaluation import EvaluationResponse

class ClassBase(BaseModel):
    semester: str
    schedule: str
    vacancies: int

class ClassCreate(ClassBase):
    discipline_id: int
    professor_id: int

class ClassUpdate(BaseModel):
    semester: Optional[str] = None
    schedule: Optional[str] = None
    vacancies: Optional[int] = None
    discipline_id: Optional[int] = None
    professor_id: Optional[int] = None

class ClassResponse(ClassBase):
    id: int
    discipline: DisciplineResponse
    professor: UserResponse
    evaluations: list[EvaluationResponse]

    model_config = ConfigDict(from_attributes=True)