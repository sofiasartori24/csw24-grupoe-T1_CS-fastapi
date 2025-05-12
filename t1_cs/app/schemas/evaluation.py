from pydantic import BaseModel, ConfigDict
from datetime import date

class EvaluationBase(BaseModel):
    date: date
    statement: str
    type: str

class EvaluationCreate(EvaluationBase):
    class_id: int

class EvaluationResponse(EvaluationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)