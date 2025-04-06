from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
import os
import json
from datetime import datetime

# Inicjalizacja aplikacji FastAPI
app = FastAPI(
    title="Todo API",
    description="Proste API do zarządzania zadaniami",
    version="1.0.0"
)

# Modele danych
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True

# Inicjalizacja bazy danych SQLite
DB_PATH = "todo.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Inicjalizacja bazy danych
init_db()

# Funkcje pomocnicze
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Endpointy
@app.get("/")
def read_root():
    return {"message": "Witaj w Todo API"}

@app.get("/todos", response_model=List[Todo])
def read_todos(db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY id")
    todos = cursor.fetchall()
    return [dict(todo) for todo in todos]

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    if todo is None:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    return dict(todo)

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db = Depends(get_db)):
    cursor = db.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO todos (title, description, completed, created_at) VALUES (?, ?, ?, ?)",
        (todo.title, todo.description, todo.completed, created_at)
    )
    db.commit()
    todo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    new_todo = cursor.fetchone()
    return dict(new_todo)

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    
    cursor.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (todo.title, todo.description, todo.completed, todo_id)
    )
    db.commit()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    updated_todo = cursor.fetchone()
    return dict(updated_todo)

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return None

