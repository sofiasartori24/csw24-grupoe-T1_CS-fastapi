from pydantic import BaseModel, ConfigDict
from typing import Optional

class ResourceTypeBase(BaseModel):
    name: str

class ResourceTypeCreate(ResourceTypeBase):
    pass

class ResourceTypeUpdate(BaseModel):
    name: Optional[str] = None  
class ResourceTypeResponse(ResourceTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

ResourceTypeResponse.update_forward_refs()
