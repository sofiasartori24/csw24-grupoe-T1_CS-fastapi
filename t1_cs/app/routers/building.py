from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.building import BuildingService
from app.schemas.building import BuildingCreate, BuildingResponse

router = APIRouter(prefix="/buildings", tags=["Buildings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[BuildingResponse])
def get_buildings(db: Session = Depends(get_db)):
    return BuildingService.get_all_buildings(db)

@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = BuildingService.get_building_by_id(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.post("/", response_model=BuildingResponse)
def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    return BuildingService.create_building(db, building)

@router.delete("/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    building = BuildingService.delete_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building deleted successfully"}