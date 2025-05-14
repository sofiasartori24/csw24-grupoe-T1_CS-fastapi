# -*- coding: utf-8 -*-

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.services.user import UserService

def get_current_user(db: Session = Depends(lambda: SessionLocal())) -> User:
    user_id = 2  
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="nao econtrado")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.profile.name.lower() != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem acessar")
    return user

def require_professor(user: User = Depends(get_current_user)):
    if user.profile.name.lower() != "professor":
        raise HTTPException(status_code=403, detail="Apenas professores podem acessar")
    return user

def require_coordinator(user: User = Depends(get_current_user)):
    if user.profile.name.lower() != "coordenador":
        raise HTTPException(status_code=403, detail="Apenas coordenadores podem acessar")
    return user
