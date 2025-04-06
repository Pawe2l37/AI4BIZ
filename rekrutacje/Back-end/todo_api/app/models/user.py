from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """Model użytkownika w bazie danych."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Relacja jeden-do-wielu z modelem Task
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan") 