from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Kontekst do hashowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Algorytm używany do tworzenia i weryfikacji tokenów JWT
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tworzy token JWT dla użytkownika.
    
    Args:
        data: Dane do zapisania w tokenie.
        expires_delta: Opcjonalny czas ważności tokenu.
        
    Returns:
        Zakodowany token JWT.
    """
    to_encode = data.copy()
    
    # Ustawienie czasu ważności tokenu
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
    to_encode.update({"exp": expire})
    
    # Zakodowanie tokenu
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Weryfikuje, czy podane hasło zgadza się z zahashowanym.
    
    Args:
        plain_password: Hasło w czystej postaci.
        hashed_password: Zahashowane hasło.
        
    Returns:
        True, jeśli hasła się zgadzają, False w przeciwnym wypadku.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashuje podane hasło.
    
    Args:
        password: Hasło do zahashowania.
        
    Returns:
        Zahashowane hasło.
    """
    return pwd_context.hash(password) 