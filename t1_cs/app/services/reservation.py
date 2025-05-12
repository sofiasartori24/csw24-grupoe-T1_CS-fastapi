from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.reservation import ReservationRepository
from app.repositories.resource import ResourceRepository
from app.schemas.reservation import ReservationCreate
from app.models.resource import ResourceStatus

class ReservationService:
    @staticmethod
    # makes a reservation (only if resource is available) then updates resource status
    def make_reservation(db: Session, reservation: ReservationCreate):
        # checks if resource is available
        resource = ResourceRepository.get_by_id(db, reservation.resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        if resource.status != ResourceStatus.available:
            raise HTTPException(status_code=400, detail="Resource is not available")

        # create reservation
        db_reservation = ReservationRepository.create(db, reservation)

        # update resource status to taken
        resource.status = ResourceStatus.taken
        db.commit()

        return db_reservation