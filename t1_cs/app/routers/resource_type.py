from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.resource_type import ResourceTypeService
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeResponse, ResourceTypeUpdate

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

        @self.router.post("/", response_model=ResourceTypeResponse)
        def create_resource_type(resource_type: ResourceTypeCreate, db: Session = Depends(get_db)):
            service = ResourceTypeService(db)
            return service.create_resource_type(resource_type)

        @self.router.put("/{resource_type_id}", response_model=ResourceTypeResponse)
        def update_resource_type(resource_type_id: int, resource_type_update: ResourceTypeUpdate, db: Session = Depends(get_db)):
            service = ResourceTypeService(db)
            return service.update_resource_type(resource_type_id, resource_type_update)

        @self.router.delete("/{resource_type_id}")
        def delete_resource_type(resource_type_id: int, db: Session = Depends(get_db)):
            service = ResourceTypeService(db)
            return service.delete_resource_type(resource_type_id)

# Instanciando e criando o router
resource_type_router = ResourceTypeRouter()
