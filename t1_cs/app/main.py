from app.database import init_db
from fastapi import FastAPI
from app.routers.reservation import ReservationRouter
from app.routers.profile import ProfileRouter
from app.routers.user import UserRouter
from app.routers.building import BuildingRouter
from app.routers.resource_type import ResourceTypeRouter
from app.routers.evaluation import EvaluationRouter
from app.routers.curriculum import CurriculumRouter
from app.routers.discipline import DisciplineRouter
from app.routers.room import RoomRouter
from app.routers.class_router import ClassRouter
from app.routers.lesson import LessonRouter
from app.routers.resource import ResourceRouter

app = FastAPI()

init_db()

reservation = ReservationRouter()
app.include_router(reservation.router)

resource = ResourceRouter()
app.include_router(resource.router)

lesson = LessonRouter()
app.include_router(lesson.router)

class_router = ClassRouter()
app.include_router(class_router.router)

room = RoomRouter()
app.include_router(room.router)

discipline = DisciplineRouter()
app.include_router(discipline.router)

curriculum = CurriculumRouter()
app.include_router(curriculum.router)

evaluation = EvaluationRouter()
app.include_router(evaluation.router)

resource_type = ResourceTypeRouter()
app.include_router(resource_type.router)

user = UserRouter()
app.include_router(user.router)

profile = ProfileRouter()
app.include_router(profile.router)

building = BuildingRouter()
app.include_router(building.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}