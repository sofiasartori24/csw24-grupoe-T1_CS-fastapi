import os
import time
import logging
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, DatabaseError

# Configure logging
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)

# Get database connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "resources_management")

# Connection retry settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Construct the database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# Configure SQLAlchemy engine with connection pooling optimized for serverless
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=5,         # Limit pool size for Lambda environment
    max_overflow=10,     # Allow up to 10 connections beyond pool_size
    connect_args={
        "connect_timeout": 5  # 5 second connection timeout
    }
)

# Add event listeners for connection debugging
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connection established")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("Database connection checked out from pool")

@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    logger.debug("Database connection returned to pool")

# Create sessionmaker with engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

def get_db_with_retry():
    """
    Get a database session with retry logic for connection issues.
    
    Returns:
        SQLAlchemy session
    
    Raises:
        Exception: If all connection attempts fail
    """
    last_exception = None
    
    for attempt in range(MAX_RETRIES):
        try:
            db = SessionLocal()
            # Test the connection with a simple query
            db.execute(text("SELECT 1"))
            return db
        except (OperationalError, DatabaseError) as e:
            last_exception = e
            if db:
                db.close()
            
            wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
            logger.warning(
                f"Database connection failed (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}. "
                f"Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
    
    # If we get here, all retries failed
    logger.error(f"All database connection retries failed. Last error: {str(last_exception)}")
    raise last_exception

def init_db():
    """
    Initialize the database schema.
    Creates all tables defined in the models.
    """
    try:
        logger.info("Initializing database schema...")
        from app import models
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database schema: {str(e)}")
        raise
