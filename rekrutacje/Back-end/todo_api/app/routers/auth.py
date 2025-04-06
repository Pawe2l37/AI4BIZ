from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import ALGORITHM, create_access_token, verify_password
from app.models.user import User
from app.schemas.user import Token, TokenData

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def authenticate_user(db: Session, username: str, password: str) -> Any:
    """
    Uwierzytelnia użytkownika na podstawie nazwy użytkownika i hasła.
    
    Args:
        db: Sesja bazy danych.
        username: Nazwa użytkownika.
        password: Hasło.
        
    Returns:
        Obiekt użytkownika, jeśli uwierzytelnienie się powiedzie, None w przeciwnym wypadku.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Pobiera aktualnego użytkownika na podstawie tokenu JWT.
    
    Args:
        db: Sesja bazy danych.
        token: Token JWT.
        
    Returns:
        Obiekt użytkownika.
        
    Raises:
        HTTPException: Jeśli token jest nieprawidłowy lub użytkownik nie istnieje.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nieprawidłowe dane uwierzytelniające",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Dekodowanie tokenu
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
        
    # Pobranie użytkownika z bazy danych
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nieaktywny użytkownik"
        )
        
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Loguje użytkownika i zwraca token dostępu.
    
    Args:
        db: Sesja bazy danych.
        form_data: Dane formularza logowania.
        
    Returns:
        Token dostępu.
        
    Raises:
        HTTPException: Jeśli dane logowania są nieprawidłowe.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowa nazwa użytkownika lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Utworzenie tokenu dostępu
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"} 