from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationCreate,  ReservationResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ReservationRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/reservations", tags=["Reservations"])
        self.add_routes()

    def add_routes(self):
        @self.router.post("/make_reservation", response_model=ReservationResponse)
        def make_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
            service = ReservationService(db)
            return service.make_reservation(reservation)
        
        @self.router.delete("/cancel_reservation/{reservation_id}", response_model=dict)
        def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
            service = ReservationService(db)
            return service.cancel_reservation(reservation_id)

        @self.router.get("/", response_model=list[ReservationResponse])
        def get_all_reservations(db: Session = Depends(get_db)):
            service = ReservationService(db)
            return service.get_all_reservations()

        @self.router.get("/{reservation_id}", response_model=ReservationResponse)
        def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
            service = ReservationService(db)
            return service.get_reservation_by_id(reservation_id)

