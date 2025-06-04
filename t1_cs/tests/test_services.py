import pytest
from app.services.user import UserService
from app.models.user import User
from app.models.profile import Profile
from datetime import date
from fastapi import HTTPException

def test_get_all_users(test_db):
    """Test the get_all_users method of UserService."""
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
    
    # Test the service
    service = UserService()
    result = service.get_all_users(test_db)
    
    # Check the result
    assert len(result) == 2
    assert result[0].email == "user1@example.com"
    assert result[1].email == "user2@example.com"

def test_get_user_by_id(test_db):
    """Test the get_user_by_id method of UserService."""
    # Create a profile
    profile = Profile(name="Test Profile")
    test_db.add(profile)
    test_db.commit()
    
    # Create a user
    user = User(email="test@example.com", name="Test User", birth_date=date(1990, 1, 1), gender="Male", profile_id=profile.id)
    test_db.add(user)
    test_db.commit()
    
    # Test the service
    service = UserService()
    result = service.get_user_by_id(test_db, user.id)
    
    # Check the result
    assert result.id == user.id
    assert result.email == "test@example.com"
    
    # Test with non-existent ID
    with pytest.raises(HTTPException) as excinfo:
        service.get_user_by_id(test_db, 999)
    assert excinfo.value.status_code == 404