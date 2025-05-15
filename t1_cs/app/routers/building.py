from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.building import BuildingService
from app.schemas.building import BuildingCreate, BuildingResponse, BuildingUpdate
from app.dependencies.permissions import require_admin
from app.services.user import UserService

class BuildingRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/buildings", tags=["Buildings"])
        self.add_routes()
        self.service = BuildingService()

    def add_routes(self):
        @self.router.get("/", response_model=list[BuildingResponse])
        def get_buildings(db: Session = Depends(self.get_db)):
            return self.service.get_all_buildings(db)

        @self.router.get("/{building_id}", response_model=BuildingResponse)
        def get_building(building_id: int, db: Session = Depends(self.get_db)):
            building = self.service.get_building_by_id(db, building_id)
            return building

        @self.router.post("/{user_id}", response_model=BuildingResponse)
        def create_building(user_id: int, building: BuildingCreate, db: Session = Depends(self.get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            require_admin(user)
            return self.service.create_building(db, building)

        @self.router.put("/{building_id}/{user_id}", response_model=BuildingResponse)
        def update_building(building_id: int, user_id: int, building_update: BuildingUpdate, db: Session = Depends(self.get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            require_admin(user)
            return self.service.update_building(db, building_id, building_update)

        @self.router.delete("/{building_id}/{user_id}")
        def delete_building(building_id: int, user_id: int, db: Session = Depends(self.get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            require_admin(user)
            return self.service.delete_building(db, building_id)

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
