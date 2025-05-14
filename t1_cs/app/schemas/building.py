from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BuildingBase(BaseModel):
    name: str
    building_number: int
    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str = Field(max_length=2, description="State abbreviation (e.g., NY)")
    postal_code: str

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BuildingBase):
    name: Optional[str] = None
    building_number: Optional[int] = None
    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = Field(max_length=2, description="State abbreviation (e.g., NY)", default=None)
    postal_code: Optional[str] = None

class BuildingResponse(BuildingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

BuildingResponse.update_forward_refs()
