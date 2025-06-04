from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class EvaluationBase(BaseModel):
    date: date
    statement: str
    type: str

class EvaluationCreate(EvaluationBase):
    class_id: int
    
class EvaluationUpdate(EvaluationBase):
    statement: Optional[str] = None
    type: Optional[str] = None

class EvaluationResponse(EvaluationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)