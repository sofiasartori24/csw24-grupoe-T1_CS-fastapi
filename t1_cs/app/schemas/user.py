from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

from app.schemas.profile import ProfileResponse

class UserBase(BaseModel):
    email: str
    name: str
    birth_date: date
    gender: str

class UserCreate(UserBase):
    profile_id: int

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    profile_id: Optional[int] = None
    
class UserResponse(UserBase):
    id: int
    profile: ProfileResponse

    model_config = ConfigDict(from_attributes=True)