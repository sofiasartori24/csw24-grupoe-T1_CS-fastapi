from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate

class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Resource).all()

    def get_by_id(self, resource_id: int):
        return self.db.query(Resource).filter(Resource.id == resource_id).first()

    def create(self, resource: ResourceCreate):
        db_resource = Resource(**resource.dict())
        self.db.add(db_resource)
        self.db.commit()
        self.db.refresh(db_resource)
        return db_resource

    def delete(self, resource_id: int):
        db_resource = self.db.query(Resource).filter(Resource.id == resource_id).first()
        if db_resource:
            self.db.delete(db_resource)
            self.db.commit()
        return db_resource

    def update(self, resource_id: int, resource_data: ResourceUpdate):
        db_resource = self.db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            return None  
        for field, value in resource_data.dict().items():
            setattr(db_resource, field, value)
        self.db.commit()
        self.db.refresh(db_resource)
        return db_resource
