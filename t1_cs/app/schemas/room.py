from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.building import BuildingResponse
from app.schemas.resource import ResourceResponse

class RoomBase(BaseModel):
    room_number: int
    capacity: int
    floor: str

class RoomCreate(RoomBase):
    building_id: int
    resource_ids: list[int] = []
    
class RoomUpdate(BaseModel):
    room_number: Optional[int] = None
    capacity: Optional[int] = None
    floor: Optional[str] = None
    building_id: Optional[int] = None
    resource_ids: Optional[List[int]] = None

class RoomResponse(RoomBase):
    id: int
    building: BuildingResponse
    resources: list[ResourceResponse]

    model_config = ConfigDict(from_attributes=True)
