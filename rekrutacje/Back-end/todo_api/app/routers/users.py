from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, db: Session = Depends(get_db)
) -> Any:
    """
    Tworzy nowego użytkownika.
    
    Args:
        user_in: Dane nowego użytkownika.
        db: Sesja bazy danych.
        
    Returns:
        Utworzony użytkownik.
        
    Raises:
        HTTPException: Jeśli użytkownik o podanym emailu lub nazwie użytkownika już istnieje.
    """
    # Sprawdzenie, czy użytkownik o podanym emailu już istnieje
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Użytkownik o podanym adresie email już istnieje."
        )
        
    # Sprawdzenie, czy użytkownik o podanej nazwie użytkownika już istnieje
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Użytkownik o podanej nazwie użytkownika już istnieje."
        )
        
    # Utworzenie nowego użytkownika
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active
    )
    
    # Zapisanie użytkownika w bazie danych
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Pobiera dane aktualnie zalogowanego użytkownika.
    
    Args:
        current_user: Aktualnie zalogowany użytkownik.
        
    Returns:
        Dane użytkownika.
    """
    return current_user 