from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource import ResourceService
from app.schemas.resource import ResourceCreate, ResourceResponse, ResourceUpdate
from app.dependencies.permissions import require_admin

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

    def add_routes(self):
        @self.router.get("/", response_model=list[ResourceResponse])
        def get_resources(db: Session = Depends(get_db)):
            service = ResourceService(db)
            return service.get_all_resources()

        @self.router.get("/{resource_id}", response_model=ResourceResponse)
        def get_resource_by_id(resource_id: int, db: Session = Depends(get_db)):
            service = ResourceService(db)
            resource = service.get_resource_by_id(resource_id)
            if not resource:
                raise HTTPException(status_code=404, detail="Resource not found")
            return resource

        @self.router.post("/", response_model=ResourceResponse)
        def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
            service = ResourceService(db)
            return service.create_resource(resource)

        @self.router.put("/{resource_id}", response_model=ResourceResponse)
        def update_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db), user = Depends(require_admin)):
            service = ResourceService(db)
            return service.update_resource(resource_id, resource)

        @self.router.delete("/{resource_id}", response_model=dict)
        def delete_resource(resource_id: int, db: Session = Depends(get_db), user = Depends(require_admin)):
            service = ResourceService(db)
            return service.delete_resource(resource_id)
