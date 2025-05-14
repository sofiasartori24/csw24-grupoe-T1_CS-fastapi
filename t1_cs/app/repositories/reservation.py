from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, reservation: ReservationCreate):
        db_reservation = Reservation(
            lesson_id=reservation.lesson_id,
            resource_id=reservation.resource_id,
            observation=reservation.observation,
        )
        self.db.add(db_reservation)
        self.db.commit()
        self.db.refresh(db_reservation)
        return db_reservation

    def get_all(self):
        return self.db.query(Reservation).all()

    def get_by_id(self, reservation_id: int):
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def delete(self, reservation_id: int):
        db_reservation = self.get_by_id(reservation_id)
        if db_reservation:
            self.db.delete(db_reservation)
            self.db.commit()
            return True
        return False
