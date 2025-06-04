import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient
import os

# Set test database URL - use in-memory SQLite for isolated tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    # Use in-memory SQLite for testing
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    yield engine

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a test database session with clean tables for each test."""
    # Create all tables for this test
    Base.metadata.create_all(bind=test_engine)
    
    # Create a new session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        # Clean up after test
        db.rollback()
        db.close()
        # Drop all tables to ensure a clean state for the next test
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c