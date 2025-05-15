from sqlalchemy.orm import Session
from app.repositories.resource import ResourceRepository
from app.schemas.resource import ResourceCreate, ResourceUpdate
from fastapi import HTTPException

class ResourceService:
    def __init__(self):
        self.repository = ResourceRepository()

    def get_all_resources(self, db: Session):
        resources = self.repository.get_all(db)
        if not resources:
            raise HTTPException(status_code=404, detail="No resources found")
        return resources

    def get_resource_by_id(self, db: Session, resource_id: int):
        resource = self.repository.get_by_id(db, resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return resource

    def create_resource(self, db: Session, resource_data: ResourceCreate):
        return self.repository.create(db, resource_data)

    def delete_resource(self, db: Session, resource_id: int):
        resource = self.repository.delete(db, resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return {"message": "Resource deleted successfully"}

    def update_resource(self, db: Session, resource_id: int, resource_data: ResourceUpdate):
        resource = self.repository.update(db, resource_id, resource_data)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        return resource
