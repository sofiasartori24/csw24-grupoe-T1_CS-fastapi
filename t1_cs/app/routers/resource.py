from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource import ResourceService
from app.schemas.resource import ResourceCreate, ResourceResponse

router = APIRouter(prefix="/resources", tags=["Resources"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return ResourceService.get_all_resources(db)

@router.post("/", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    return ResourceService.create_resource(db, resource)