from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource import ResourceService
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate
from app.dependencies.permissions import require_admin
from app.services.user import UserService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResourceRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/resources", tags=["Resources"])
        self.add_routes()
        self.service = ResourceService()

    def add_routes(self):
        @self.router.get("/", response_model=list[ResourceResponse])
        def get_resources(db: Session = Depends(get_db)):
            return self.service.get_all_resources(db)

        @self.router.get("/{resource_id}", response_model=ResourceResponse)
        def get_resource_by_id(resource_id: int, db: Session = Depends(get_db)):
            resource = self.service.get_resource_by_id(db, resource_id)
            if not resource:
                raise HTTPException(status_code=404, detail="Resource not found")
            return resource

        @self.router.post("/{user_id}", response_model=ResourceResponse)
        def create_resource(user_id: int, resource: ResourceCreate, db: Session = Depends(get_db)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.create_resource(db, resource)

        @self.router.put("/{resource_id}/{user_id}", response_model=ResourceResponse)
        def update_resource(resource_id: int, user_id: int, resource: ResourceUpdate, db: Session = Depends(get_db), user = Depends(require_admin)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.update_resource(db, resource_id, resource)

        @self.router.delete("/{resource_id}/{user_id}", response_model=dict)
        def delete_resource(resource_id: int, user_id: int, db: Session = Depends(get_db), user = Depends(require_admin)):
            user_service = UserService()
            user = user_service.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            return self.service.delete_resource(db, resource_id)
