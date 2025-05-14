from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.evaluation import EvaluationService
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse, EvaluationUpdate
from app.dependencies.permissions import require_professor
from app.services.user import UserService

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EvaluationRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/evaluations", tags=["Evaluations"])
        self.add_routes()

    def add_routes(self):
        @self.router.get("/", response_model=list[EvaluationResponse])
        def get_evaluations(db: Session = Depends(get_db)):
            service = EvaluationService(db)
            return service.get_all_evaluations()
        
        @self.router.get("/{evaluation_id}", response_model=EvaluationResponse)
        def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
            service = EvaluationService(db)
            return service.get_evaluation_by_id(evaluation_id)

        @self.router.post("/{user_id}", response_model=EvaluationResponse)
        def create_evaluation(user_id: int, evaluation: EvaluationCreate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = EvaluationService(db)
            return service.create_evaluation(evaluation)

        @self.router.put("/{evaluation_id}/{user_id}", response_model=EvaluationResponse)
        def update_evaluation(evaluation_id: int, user_id: int, evaluation_update: EvaluationUpdate, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = EvaluationService(db)
            return service.update_evaluation(evaluation_id, evaluation_update)

        @self.router.delete("/{evaluation_id}/{user_id}")
        def delete_evaluation(evaluation_id: int, user_id: int, db: Session = Depends(get_db)):
            user_service = UserService(db)
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            require_professor(user)
            service = EvaluationService(db)
            return service.delete_evaluation(evaluation_id)

