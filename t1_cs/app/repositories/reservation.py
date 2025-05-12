from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

class ReservationRepository:
    @staticmethod
    def create(db: Session, reservation: ReservationCreate):
        db_reservation = Reservation(
            lesson_id=reservation.lesson_id,
            resource_id=reservation.resource_id,
            observation=reservation.observation,
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation