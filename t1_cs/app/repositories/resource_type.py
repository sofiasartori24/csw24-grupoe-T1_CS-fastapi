from sqlalchemy.orm import Session
from app.models.resource_type import ResourceType
from app.schemas.resource_type import ResourceTypeCreate, ResourceTypeUpdate

class ResourceTypeRepository:
    def __init__(self):
        pass

    def get_all(self, db: Session):
        return db.query(ResourceType).all()

    def get_by_id(self, db: Session, resource_type_id: int):
        return db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()

    def create(self, db: Session, resource_type: ResourceTypeCreate):
        db_resource_type = ResourceType(**resource_type.dict())
        db.add(db_resource_type)
        db.commit()
        db.refresh(db_resource_type)
        return db_resource_type

    def update(self, db: Session, resource_type_id: int, resource_type_update: ResourceTypeUpdate):
        db_resource_type = db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
        if db_resource_type:
            for var, value in resource_type_update.dict(exclude_unset=True).items():
                setattr(db_resource_type, var, value)
            db.commit()
            db.refresh(db_resource_type)
        return db_resource_type

    def delete(self, db: Session, resource_type_id: int):
        db_resource_type = db.query(ResourceType).filter(ResourceType.id == resource_type_id).first()
        if db_resource_type:
            db.delete(db_resource_type)
            db.commit()
        return db_resource_type
