# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserResponse


def require_admin(user: UserResponse):
    if user.profile.name.lower() != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem acessar")
    return user

def require_professor(user: UserResponse):
    if user.profile.name.lower() != "professor":
        raise HTTPException(status_code=403, detail="Apenas professores podem acessar")
    return user

def require_coordinator(user: UserResponse):
    print(user.profile.name.lower())
    if user.profile.name.lower() != "coordinator":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem acessar")
    return user
