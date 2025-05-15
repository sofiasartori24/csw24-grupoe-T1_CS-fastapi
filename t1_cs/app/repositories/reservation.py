from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

class ReservationRepository:
    def __init__(self):
        pass

    def create(self, db: Session, reservation: ReservationCreate):
        db_reservation = Reservation(
            lesson_id=reservation.lesson_id,
            resource_id=reservation.resource_id,
            observation=reservation.observation,
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    def get_all(self, db: Session):
        return db.query(Reservation).all()

    def get_by_id(self, db: Session, reservation_id: int):
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def delete(self, db: Session, reservation_id: int):
        db_reservation = self.get_by_id(db, reservation_id)
        if db_reservation:
            db.delete(db_reservation)
            db.commit()
            return True
        return False
