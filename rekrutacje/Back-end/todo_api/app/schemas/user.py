from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Schemat bazowy dla użytkownika
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    is_active: Optional[bool] = True


# Schemat dla tworzenia nowego użytkownika
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


# Schemat dla aktualizacji użytkownika
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


# Schemat dla wyświetlania użytkownika
class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# Schemat dla tokenu dostępu
class Token(BaseModel):
    access_token: str
    token_type: str


# Schemat dla danych zawartych w tokenie
class TokenData(BaseModel):
    username: Optional[str] = None 