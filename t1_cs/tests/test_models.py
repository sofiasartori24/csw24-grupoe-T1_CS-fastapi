import pytest
from app.models.user import User
from app.models.profile import Profile
from datetime import date

def test_user_model(test_db):
    """Test the User model."""
    # Create a profile
    profile = Profile(name="Test Profile")
    test_db.add(profile)
    test_db.commit()
    
    # Create a user
    user = User(
        email="test@example.com",
        name="Test User",
        birth_date=date(1990, 1, 1),
        gender="Male",
        profile_id=profile.id
    )
    test_db.add(user)
    test_db.commit()
    
    # Retrieve the user from the database
    db_user = test_db.query(User).filter(User.email == "test@example.com").first()
    
    # Check user attributes
    assert db_user.email == "test@example.com"
    assert db_user.name == "Test User"
    assert db_user.birth_date == date(1990, 1, 1)
    assert db_user.gender == "Male"
    assert db_user.profile_id == profile.id

def test_profile_model(test_db):
    """Test the Profile model."""
    # Create a profile
    profile = Profile(name="Admin")
    test_db.add(profile)
    test_db.commit()
    
    # Retrieve the profile from the database
    db_profile = test_db.query(Profile).filter(Profile.name == "Admin").first()
    
    # Check profile attributes
    assert db_profile.name == "Admin"