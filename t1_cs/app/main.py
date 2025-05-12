from app.database import init_db
from fastapi import FastAPI
from app.routers import user, profile, building, discipline, curriculum, lesson
from app.routers import evaluation, class_router, resource_type, resource, room, reservation

app = FastAPI()

init_db()

app.include_router(reservation.router)
app.include_router(resource.router)
app.include_router(lesson.router)
app.include_router(class_router.router)
app.include_router(room.router)
app.include_router(user.router)
app.include_router(building.router)
app.include_router(discipline.router)
app.include_router(curriculum.router)
app.include_router(evaluation.router)
app.include_router(resource_type.router)
app.include_router(profile.router)



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}