from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Schemat bazowy dla zadania
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None


# Schemat dla tworzenia nowego zadania
class TaskCreate(TaskBase):
    pass


# Schemat dla aktualizacji zadania
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# Schemat dla wyświetlania zadania
class Task(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    
    class Config:
        orm_mode = True 