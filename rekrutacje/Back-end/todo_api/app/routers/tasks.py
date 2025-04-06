from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.task import Task as TaskSchema
from app.schemas.task import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Tworzy nowe zadanie dla zalogowanego użytkownika.
    
    Args:
        task_in: Dane nowego zadania.
        db: Sesja bazy danych.
        current_user: Aktualnie zalogowany użytkownik.
        
    Returns:
        Utworzone zadanie.
    """
    # Utworzenie nowego zadania
    task = Task(
        **task_in.dict(),
        owner_id=current_user.id
    )
    
    # Zapisanie zadania w bazie danych
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.get("", response_model=List[TaskSchema])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Pobiera wszystkie zadania zalogowanego użytkownika.
    
    Args:
        skip: Liczba zadań do pominięcia.
        limit: Maksymalna liczba zadań do pobrania.
        db: Sesja bazy danych.
        current_user: Aktualnie zalogowany użytkownik.
        
    Returns:
        Lista zadań.
    """
    tasks = (
        db.query(Task)
        .filter(Task.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return tasks


@router.get("/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Pobiera zadanie o podanym identyfikatorze.
    
    Args:
        task_id: Identyfikator zadania.
        db: Sesja bazy danych.
        current_user: Aktualnie zalogowany użytkownik.
        
    Returns:
        Zadanie.
        
    Raises:
        HTTPException: Jeśli zadanie nie istnieje lub nie należy do zalogowanego użytkownika.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    # Sprawdzenie, czy zadanie istnieje
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zadanie nie istnieje."
        )
        
    # Sprawdzenie, czy zadanie należy do zalogowanego użytkownika
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak dostępu do tego zadania."
        )
        
    return task


@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Aktualizuje zadanie o podanym identyfikatorze.
    
    Args:
        task_id: Identyfikator zadania.
        task_in: Dane do aktualizacji.
        db: Sesja bazy danych.
        current_user: Aktualnie zalogowany użytkownik.
        
    Returns:
        Zaktualizowane zadanie.
        
    Raises:
        HTTPException: Jeśli zadanie nie istnieje lub nie należy do zalogowanego użytkownika.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    # Sprawdzenie, czy zadanie istnieje
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zadanie nie istnieje."
        )
        
    # Sprawdzenie, czy zadanie należy do zalogowanego użytkownika
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak dostępu do tego zadania."
        )
    
    # Aktualizacja zadania
    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
        
    # Zapisanie zmian w bazie danych
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Usuwa zadanie o podanym identyfikatorze.
    
    Args:
        task_id: Identyfikator zadania.
        db: Sesja bazy danych.
        current_user: Aktualnie zalogowany użytkownik.
        
    Raises:
        HTTPException: Jeśli zadanie nie istnieje lub nie należy do zalogowanego użytkownika.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    # Sprawdzenie, czy zadanie istnieje
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zadanie nie istnieje."
        )
        
    # Sprawdzenie, czy zadanie należy do zalogowanego użytkownika
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brak dostępu do tego zadania."
        )
        
    # Usunięcie zadania z bazy danych
    db.delete(task)
    db.commit()
    
    return None 