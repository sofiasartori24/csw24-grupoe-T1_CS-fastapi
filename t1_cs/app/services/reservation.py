from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.reservation import ReservationRepository
from app.repositories.resource import ResourceRepository
from app.schemas.reservation import ReservationCreate
from app.models.resource import ResourceStatus

class ReservationService:
    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.resource_repository = ResourceRepository()

    def make_reservation(self, db: Session, reservation: ReservationCreate):
        # checks if resource is available
        resource = self.resource_repository.get_by_id(db, reservation.resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        if resource.status != ResourceStatus.available:
            raise HTTPException(status_code=400, detail="Resource is not available")

        # create reservation
        db_reservation = self.reservation_repository.create(db, reservation)

        # update resource status to taken
        resource.status = ResourceStatus.taken
        db.commit()

        return db_reservation

    def cancel_reservation(self, db: Session, reservation_id: int):
        # Get reservation
        reservation = self.reservation_repository.get_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        # Delete the reservation
        success = self.reservation_repository.delete(db, reservation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Failed to cancel reservation")

        # Update resource status to available
        resource = self.resource_repository.get_by_id(db, reservation.resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        resource.status = ResourceStatus.available
        self.db.commit()

        return {"message": "Reservation cancelled successfully, and resource status updated to available."}

    def get_reservation_by_id(self, db: Session, reservation_id: int):
        reservation = self.reservation_repository.get_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return reservation

    def get_all_reservations(self, db: Session):
        return self.reservation_repository.get_all(db)
