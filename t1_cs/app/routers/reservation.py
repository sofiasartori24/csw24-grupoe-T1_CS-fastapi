from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationCreate,  ReservationResponse
from app.services.user import UserService
from app.dependencies.permissions import require_professor

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
        @self.router.post("/make_reservation/{user_id}", response_model=ReservationResponse)
        def make_reservation(user_id: int, reservation: ReservationCreate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = ReservationService(db)
            return service.make_reservation(reservation)
        
        @self.router.delete("/cancel_reservation/{reservation_id}/{user_id}", response_model=dict)
        def cancel_reservation(user_id: int, reservation_id: int, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
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

