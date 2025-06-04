import pytest
from sqlalchemy import text

def test_database_connection(test_engine):
    """Test that the database connection works."""
    # Test direct engine connection
    with test_engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1

def test_database_session(test_db):
    """Test that the database session works."""
    result = test_db.execute(text("SELECT 1")).scalar()
    assert result == 1