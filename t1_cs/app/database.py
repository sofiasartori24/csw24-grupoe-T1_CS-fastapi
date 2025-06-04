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
MAX_RETRIES = 5  # Increased from 3
RETRY_DELAY = 1  # seconds

# Log database connection info (without password)
logger.info(f"Database configuration: Host={DB_HOST}, User={DB_USER}, Database={DB_NAME}")

# Construct the database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# Log when the database URL is constructed (without showing the password)
masked_url = f"mysql+pymysql://{DB_USER}:****@{DB_HOST}:3306/{DB_NAME}"
logger.info(f"Database URL: {masked_url}")

# Configure SQLAlchemy engine with connection pooling optimized for serverless
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=300,    # Recycle connections after 5 minutes (reduced from 1 hour)
    pool_size=5,         # Limit pool size for Lambda environment
    max_overflow=10,     # Allow up to 10 connections beyond pool_size
    connect_args={
        "connect_timeout": 20,  # 20 second connection timeout (increased from 10)
        "read_timeout": 30,     # 30 second read timeout
        "write_timeout": 30,    # 30 second write timeout
        "ssl": {"ssl_mode": "REQUIRED"}  # Enable SSL for secure connections
    }
)

# Log when the engine is created
logger.info("SQLAlchemy engine created with connection pooling")

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
    db = None
    
    for attempt in range(MAX_RETRIES):
        try:
            # Close any existing connection that might be in a bad state
            if db:
                try:
                    db.close()
                except Exception as close_error:
                    logger.warning(f"Error closing database connection: {str(close_error)}")
                db = None
            
            # Create a new session
            db = SessionLocal()
            
            # Test the connection with a simple query
            logger.info(f"Testing database connection (attempt {attempt+1})...")
            result = db.execute(text("SELECT 1")).scalar()
            logger.info(f"Database connection successful (attempt {attempt+1}). Test query result: {result}")
            return db
            
        except (OperationalError, DatabaseError) as e:
            last_exception = e
            
            # Calculate wait time with exponential backoff and some jitter
            base_wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
            jitter = base_wait_time * 0.2 * (0.5 - time.time() % 0.5)  # Add up to 20% jitter
            wait_time = base_wait_time + jitter
            
            logger.warning(
                f"Database connection failed (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}. "
                f"Host: {DB_HOST}, Database: {DB_NAME}. "
                f"Retrying in {wait_time:.2f} seconds..."
            )
            time.sleep(wait_time)
        except Exception as e:
            # Handle unexpected exceptions
            logger.error(f"Unexpected error connecting to database: {str(e)}")
            if db:
                try:
                    db.close()
                except:
                    pass
            raise
    
    # If we get here, all retries failed
    logger.error(f"All database connection retries ({MAX_RETRIES}) failed. Last error: {str(last_exception)}")
    
    # Include more diagnostic information in the exception
    error_message = (
        f"Failed to connect to database after {MAX_RETRIES} attempts. "
        f"Host: {DB_HOST}, Database: {DB_NAME}, User: {DB_USER}. "
        f"Connection timeout: 20 seconds. "
        f"Last error: {str(last_exception)}"
    )
    raise OperationalError(error_message, None, last_exception)

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
