from app.database import SessionLocal, init_db, get_db_with_retry
from sqlalchemy import text
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
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
from app.script import populate_profiles_and_user, populate_all
import logging
import os
import time
import traceback
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DatabaseError
import pymysql
from fastapi.middleware.cors import CORSMiddleware  # Import necessário para CORS

# Configure logging
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

# Determine if we're running in AWS Lambda
is_lambda = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
# Get the API stage name (default to "Prod" if not specified)
api_stage = os.environ.get("API_STAGE", "Prod")

# Configure FastAPI app with appropriate OpenAPI URL
if is_lambda:
    openapi_url = f"/{api_stage}/openapi.json"
    logger.info(f"Running in Lambda environment. Setting openapi_url to: {openapi_url}")
    app = FastAPI(openapi_url=openapi_url)

    @app.get("/openapi.json")
    async def get_openapi_schema():
        return app.openapi()
else:
    logger.info("Running in local environment. Using default OpenAPI URL.")
    app = FastAPI()

# Enhanced CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    # Allow specific origins or use ["*"] for any origin
    allow_origins=["http://localhost:3000", "*"],
    # Set to False for DELETE requests to work properly with credentials
    allow_credentials=False,
    # Explicitly list all allowed methods to ensure OPTIONS is included
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    # Allow all headers
    allow_headers=["*"],
    # Allow browsers to cache preflight results longer
    max_age=86400,  # 24 hours
    # Expose these headers to the browser
    expose_headers=["Content-Type", "X-Requested-With", "Authorization"]
)

# Configure OpenAPI schema com o servidor correto
def custom_openapi():
    from fastapi.openapi.utils import get_openapi

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI Application",
        version="1.0.0",
        description="API for resource management system",
        routes=app.routes,
    )

    if is_lambda:
        openapi_schema["servers"] = [{"url": f"/{api_stage}"}]
        logger.info(f"Setting OpenAPI server URL to: /{api_stage}")
    else:
        openapi_schema["servers"] = [{"url": ""}]
        logger.info("Using default server URL for local development")

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Database dependency with retry logic
def get_db():
    db = None
    try:
        db = get_db_with_retry()
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        if db:
            db.close()
        raise
    finally:
        if db:
            db.close()

# Middleware para lidar com erros de banco de dados
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except (SQLAlchemyError, OperationalError, DatabaseError, pymysql.Error) as e:
        logger.error(f"Database error in request: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error", "message": str(e)},
        )
    except Exception as e:
        logger.error(f"Request failed: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "message": str(e)},
        )

# Endpoint admin para inicializar banco de dados
@app.post("/admin/init-db")
def initialize_database(db: Session = Depends(get_db)):
    try:
        init_db()
        populate_profiles_and_user(db)
        populate_all(db)
        return {"message": "Database initialized successfully"}
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database initialization failed", "message": str(e)},
        )

# Health check
@app.get("/health")
def health_check():
    try:
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=200,
            content={"status": "healthy"}
        )

# Checagem de status do banco
@app.get("/db-status")
def db_status(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "connected", "result": result}
    except Exception as e:
        logger.error(f"Database status check failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "disconnected", "error": str(e)},
        )

# Routers incluídos
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

# Root endpoint
@app.get("/")
def read_root():
    try:
        return {"message": "Hello, World!"}
    except Exception as e:
        logger.error(f"Root endpoint error: {str(e)}")
        return JSONResponse(
            status_code=200,
            content={"message": "Hello, World!"}
        )

# Test route
@app.get("/test-route")
def test_route():
    try:
        return {"message": "Test route is working!", "status": "success"}
    except Exception as e:
        logger.error(f"Test route error: {str(e)}")
        return JSONResponse(
            status_code=200,
            content={"message": "Test route error", "error": str(e)}
        )
