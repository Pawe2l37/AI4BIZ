import secrets
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    """Klasa przechowująca ustawienia aplikacji."""
    
    # Podstawowe ustawienia API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API Listy Zadań"
    
    # Ustawienia bezpieczeństwa
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dni
    
    # URL bazy danych
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./todo_app.db"


settings = Settings() 