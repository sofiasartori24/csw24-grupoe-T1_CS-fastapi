from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate

class ResourceRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(Resource).all()

    def get_by_id(self, db: Session, resource_id: int):
        return db.query(Resource).filter(Resource.id == resource_id).first()

    def create(self, db: Session, resource: ResourceCreate):
        db_resource = Resource(**resource.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource

    def delete(self, db: Session, resource_id: int):
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if db_resource:
            db.delete(db_resource)
            db.commit()
        return db_resource

    def update(self, db: Session, resource_id: int, resource_data: ResourceUpdate):
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            return None  
        for field, value in resource_data.dict().items():
            setattr(db_resource, field, value)
        db.commit()
        db.refresh(db_resource)
        return db_resource
