import pytest
from app.repositories.user import UserRepository
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserCreate, UserUpdate
from datetime import date

def test_get_all(test_db):
    """Test the get_all method of UserRepository."""
    # Create a profile
    profile = Profile(name="Test Profile")
    test_db.add(profile)
    test_db.commit()
    
    # Create users
    users = [
        User(email="user1@example.com", name="User 1", birth_date=date(1990, 1, 1), gender="Male", profile_id=profile.id),
        User(email="user2@example.com", name="User 2", birth_date=date(1991, 2, 2), gender="Female", profile_id=profile.id),
    ]
    test_db.add_all(users)
    test_db.commit()
    
    # Test the repository
    repo = UserRepository()
    result = repo.get_all(test_db)
    
    # Check the result
    assert len(result) == 2
    assert result[0].email == "user1@example.com"
    assert result[1].email == "user2@example.com"

def test_get_by_id(test_db):
    """Test the get_by_id method of UserRepository."""
    # Create a profile
    profile = Profile(name="Test Profile")
    test_db.add(profile)
    test_db.commit()
    
    # Create a user
    user = User(email="test@example.com", name="Test User", birth_date=date(1990, 1, 1), gender="Male", profile_id=profile.id)
    test_db.add(user)
    test_db.commit()
    
    # Test the repository
    repo = UserRepository()
    result = repo.get_by_id(test_db, user.id)
    
    # Check the result
    assert result.id == user.id
    assert result.email == "test@example.com"
    
    # Test with non-existent ID
    result = repo.get_by_id(test_db, 999)
    assert result is None

def test_create(test_db):
    """Test the create method of UserRepository."""
    # Create a profile
    profile = Profile(name="Test Profile")
    test_db.add(profile)
    test_db.commit()
    
    # Create user data
    user_data = UserCreate(
        email="new@example.com",
        name="New User",
        birth_date=date(1992, 3, 3),
        gender="Male",
        profile_id=profile.id
    )
    
    # Test the repository
    repo = UserRepository()
    result = repo.create(test_db, user_data)
    
    # Check the result
    assert result.id is not None
    assert result.email == "new@example.com"
    assert result.name == "New User"
    
    # Check that the user was added to the database
    db_user = test_db.query(User).filter(User.email == "new@example.com").first()
    assert db_user is not None
    assert db_user.name == "New User"