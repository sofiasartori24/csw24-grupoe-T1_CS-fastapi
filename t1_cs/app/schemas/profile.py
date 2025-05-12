from pydantic import BaseModel, ConfigDict

class ProfileBase(BaseModel):
    name: str

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int

    model_config = ConfigDict(from_attributes=True)