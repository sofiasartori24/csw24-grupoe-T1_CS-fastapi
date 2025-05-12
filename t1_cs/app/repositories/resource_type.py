from sqlalchemy.orm import Session
from app.models.resource_type import ResourceType
from app.schemas.resource_type import ResourceTypeCreate

class ResourceTypeRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(ResourceType).all()

    @staticmethod
    def get_by_id(db: Session, resource_type_id: int):
        return db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()

    @staticmethod
    def create(db: Session, resource_type: ResourceTypeCreate):
        db_resource_type = ResourceType(**resource_type.dict())
        db.add(db_resource_type)
        db.commit()
        db.refresh(db_resource_type)
        return db_resource_type

    @staticmethod
    def delete(db: Session, resource_type_id: int):
        db_resource_type = db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
        if db_resource_type:
            db.delete(db_resource_type)
            db.commit()
        return db_resource_type