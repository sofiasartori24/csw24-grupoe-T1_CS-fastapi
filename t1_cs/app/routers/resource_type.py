from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource_type import ResourceTypeService
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeResponse, ResourceTypeUpdate
from app.dependencies.permissions import require_admin
from app.services.user import UserService

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResourceTypeRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/resource-types", tags=["Resource Types"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[ResourceTypeResponse])
        def get_resource_types(db: Session = Depends(get_db)):
            service = ResourceTypeService(db)
            return service.get_all_resource_types()

        @self.router.get("/{resource_type_id}", response_model=ResourceTypeResponse)
        def get_resource_type(resource_type_id: int, db: Session = Depends(get_db)):
            service = ResourceTypeService(db)
            return service.get_resource_type_by_id(resource_type_id)

        @self.router.post("/{user_id}", response_model=ResourceTypeResponse)
        def create_resource_type(user_id: int, resource_type: ResourceTypeCreate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = ResourceTypeService(db)
            return service.create_resource_type(resource_type)

        @self.router.put("/{resource_type_id}/{user_id}", response_model=ResourceTypeResponse)
        def update_resource_type(user_id: int, resource_type_id: int, resource_type_update: ResourceTypeUpdate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = ResourceTypeService(db)
            return service.update_resource_type(resource_type_id, resource_type_update)

        @self.router.delete("/{resource_type_id}/{user_id}")
        def delete_resource_type(resource_type_id: int, user_id: int, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_admin(user)
            service = ResourceTypeService(db)
            return service.delete_resource_type(resource_type_id)

