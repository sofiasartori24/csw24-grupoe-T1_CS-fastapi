from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource_type import ResourceTypeService
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeResponse

router = APIRouter(prefix="/resource-types", tags=["Resource Types"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ResourceTypeResponse])
def get_resource_types(db: Session = Depends(get_db)):
    return ResourceTypeService.get_all_resource_types(db)

@router.post("/", response_model=ResourceTypeResponse)
def create_resource_type(resource_type: ResourceTypeCreate, db: Session = Depends(get_db)):
    return ResourceTypeService.create_resource_type(db, resource_type)