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

    def add_routes(self):
        @self.router.get("/", response_model=list[BuildingResponse])
        def get_buildings(db: Session = Depends(self.get_db)):
            service = BuildingService(db)
            return service.get_all_buildings()

        @self.router.get("/{building_id}", response_model=BuildingResponse)
        def get_building(building_id: int, db: Session = Depends(self.get_db)):
            service = BuildingService(db)
            building = service.get_building_by_id(building_id)
            return building

        @self.router.post("/{user_id}", response_model=BuildingResponse)
        def create_building(user_id: int, building: BuildingCreate, db: Session = Depends(self.get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            require_admin(user)
            service = BuildingService(db)
            return service.create_building(building)

        @self.router.put("/{building_id}/{user_id}", response_model=BuildingResponse)
        def update_building(building_id: int, user_id: int, building_update: BuildingUpdate, db: Session = Depends(self.get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            require_admin(user)
            service = BuildingService(db)
            return service.update_building(building_id, building_update)

        @self.router.delete("/{building_id}/{user_id}")
        def delete_building(building_id: int, user_id: int, db: Session = Depends(self.get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            require_admin(user)
            service = BuildingService(db)
            return service.delete_building(building_id)

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
