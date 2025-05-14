from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.reservation import ReservationRepository
from app.repositories.resource import ResourceRepository
from app.schemas.reservation import ReservationCreate
from app.models.resource import ResourceStatus

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.reservation_repository = ReservationRepository(db)
        self.resource_repository = ResourceRepository(db)

    def make_reservation(self, reservation: ReservationCreate):
        # checks if resource is available
        resource = self.resource_repository.get_by_id(reservation.resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        if resource.status != ResourceStatus.available:
            raise HTTPException(status_code=400, detail="Resource is not available")

        # create reservation
        db_reservation = self.reservation_repository.create(reservation)

        # update resource status to taken
        resource.status = ResourceStatus.taken
        self.db.commit()

        return db_reservation

    def cancel_reservation(self, reservation_id: int):
        # Get reservation
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        # Delete the reservation
        success = self.reservation_repository.delete(reservation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Failed to cancel reservation")

        # Update resource status to available
        resource = self.resource_repository.get_by_id(reservation.resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        resource.status = ResourceStatus.available
        self.db.commit()

        return {"message": "Reservation cancelled successfully, and resource status updated to available."}

    def get_reservation_by_id(self, reservation_id: int):
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return reservation

    def get_all_reservations(self):
        return self.reservation_repository.get_all()
