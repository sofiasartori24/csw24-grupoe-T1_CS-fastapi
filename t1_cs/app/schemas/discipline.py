from pydantic import BaseModel, ConfigDict

class DisciplineBase(BaseModel):
    name: str
    credits: int
    program: str
    bibliography: str

class DisciplineCreate(DisciplineBase):
    pass

class DisciplineResponse(DisciplineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)