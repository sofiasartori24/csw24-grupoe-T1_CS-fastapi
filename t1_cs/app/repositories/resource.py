from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate

class ResourceRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Resource).all()

    @staticmethod
    def get_by_id(db: Session, resource_id: int):
        return db.query(Resource).filter(Resource.id == resource_id).first()

    @staticmethod
    def create(db: Session, resource: ResourceCreate):
        db_resource = Resource(**resource.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource

    @staticmethod
    def delete(db: Session, resource_id: int):
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if db_resource:
            db.delete(db_resource)
            db.commit()
        return db_resource