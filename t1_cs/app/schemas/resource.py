from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.resource_type import ResourceTypeResponse
from enum import Enum

class ResourceStatus(str, Enum):
    available = "available"
    maintenance = "maintenance"
    taken = "taken"

class ResourceBase(BaseModel):
    description: str
    status: ResourceStatus

class ResourceCreate(ResourceBase):
    resource_type_id: int

    
class ResourceResponse(ResourceBase):
    id: int
    resource_type_id: int

    model_config = ConfigDict(from_attributes=True)

class ResourceUpdate(BaseModel):
    resource_type_id: int
    description: Optional[str] = None  
    status: Optional[ResourceStatus] = None 

    model_config = ConfigDict(from_attributes=True)
