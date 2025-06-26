#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to create an admin user directly in the database.
This is useful for bootstrapping the system when there are no admin users yet.
"""

import os
import sys
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Add the t1_cs directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "t1_cs"))

# Import required modules
from app.database import SessionLocal, get_db_with_retry, Base
from app.models.profile import Profile
from app.models.user import User

# Import all models to ensure they are registered with SQLAlchemy
import app.models.building
import app.models.class_model
import app.models.curriculum
import app.models.discipline
import app.models.evaluation
import app.models.lesson
import app.models.profile
import app.models.reservation
import app.models.resource_type
import app.models.resource
import app.models.room
import app.models.user

def create_admin_profile(db: Session) -> Profile:
    """Create an admin profile if it doesn't exist."""
    print("Checking if admin profile exists...")
    
    # Check if admin profile already exists
    admin_profile = db.query(Profile).filter(Profile.name.ilike("admin")).first()
    
    if admin_profile:
        print(f"Admin profile already exists with ID: {admin_profile.id}")
        return admin_profile
    
    # Create admin profile
    print("Creating admin profile...")
    admin_profile = Profile(name="Admin")
    db.add(admin_profile)
    db.commit()
    db.refresh(admin_profile)
    print(f"Admin profile created with ID: {admin_profile.id}")
    
    return admin_profile

def create_admin_user(db: Session, profile_id: int, email: str, name: str, 
                     birth_date: date, gender: str) -> User:
    """Create an admin user with the given details."""
    print(f"Checking if user with email {email} already exists...")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"User with email {email} already exists with ID: {existing_user.id}")
        return existing_user
    
    # Create admin user
    print(f"Creating admin user with email {email}...")
    admin_user = User(
        email=email,
        name=name,
        birth_date=birth_date,
        gender=gender,
        profile_id=profile_id
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"Admin user created with ID: {admin_user.id}")
    
    return admin_user

def main():
    """Main function to create an admin user."""
    # Default admin user details
    DEFAULT_EMAIL = "admin@example.com"
    DEFAULT_NAME = "System Administrator"
    DEFAULT_BIRTH_DATE = date(1990, 1, 1)
    DEFAULT_GENDER = "Other"
    
    # Get user input or use defaults
    email = input(f"Enter admin email [{DEFAULT_EMAIL}]: ") or DEFAULT_EMAIL
    name = input(f"Enter admin name [{DEFAULT_NAME}]: ") or DEFAULT_NAME
    
    birth_date_input = input(f"Enter admin birth date (YYYY-MM-DD) [{DEFAULT_BIRTH_DATE}]: ")
    if birth_date_input:
        try:
            year, month, day = map(int, birth_date_input.split('-'))
            birth_date = date(year, month, day)
        except (ValueError, TypeError):
            print(f"Invalid date format. Using default: {DEFAULT_BIRTH_DATE}")
            birth_date = DEFAULT_BIRTH_DATE
    else:
        birth_date = DEFAULT_BIRTH_DATE
    
    gender = input(f"Enter admin gender (Male/Female/Other) [{DEFAULT_GENDER}]: ") or DEFAULT_GENDER
    
    try:
        # Get database session
        print("Connecting to database...")
        db = get_db_with_retry()
        
        # Create admin profile
        admin_profile = create_admin_profile(db)
        
        # Create admin user
        admin_user = create_admin_user(
            db=db,
            profile_id=admin_profile.id,
            email=email,
            name=name,
            birth_date=birth_date,
            gender=gender
        )
        
        print("\nAdmin user creation successful!")
        print(f"ID: {admin_user.id}")
        print(f"Email: {admin_user.email}")
        print(f"Name: {admin_user.name}")
        print(f"Profile: {admin_profile.name} (ID: {admin_profile.id})")
        
    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()