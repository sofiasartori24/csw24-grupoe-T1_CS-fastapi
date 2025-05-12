from pydantic import BaseModel, ConfigDict

class ResourceTypeBase(BaseModel):
    name: str

class ResourceTypeCreate(ResourceTypeBase):
    pass

class ResourceTypeResponse(ResourceTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)