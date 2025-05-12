from pydantic import BaseModel, Field, ConfigDict

class BuildingBase(BaseModel):
    name: str
    building_number: int
    street: str
    number: str
    complement: str | None = None
    neighborhood: str
    city: str
    state: str = Field(max_length=2, description="State abbreviation (e.g., NY)")
    postal_code: str

class BuildingCreate(BuildingBase):
    pass

class BuildingResponse(BuildingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
BuildingResponse.update_forward_refs()