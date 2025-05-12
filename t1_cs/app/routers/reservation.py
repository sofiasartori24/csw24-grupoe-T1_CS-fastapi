from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/make_reservation", tags=["Reservations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return ReservationService.make_reservation(db, reservation)