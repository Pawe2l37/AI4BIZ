from typing import List, Optional
import sqlite3
import json
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Utworzenie aplikacji
app = FastAPI(title="Prosta Aplikacja Todo")

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

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Połączenie z bazą danych
def get_db():
    conn = sqlite3.connect("todo_simple.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Inicjalizacja bazy danych
def init_db():
    conn = sqlite3.connect("todo_simple.db")
    cursor = conn.cursor()
    
    # Tworzenie tabeli użytkowników
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    # Tworzenie tabeli zadań
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_at TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

# Inicjalizacja bazy danych
init_db()

# Funkcje pomocnicze
def get_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def create_user_db(conn, user: UserCreate):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, user.password)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Użytkownik o podanej nazwie lub emailu już istnieje"
        )

def get_todos(conn, skip: int = 0, limit: int = 100, user_id: int = None):
    cursor = conn.cursor()
    if user_id:
        cursor.execute(
            "SELECT * FROM todos WHERE user_id = ? ORDER BY id LIMIT ? OFFSET ?",
            (user_id, limit, skip)
        )
    else:
        cursor.execute("SELECT * FROM todos ORDER BY id LIMIT ? OFFSET ?", (limit, skip))
    return cursor.fetchall()

def create_todo_db(conn, todo: TodoCreate, user_id: int):
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO todos (title, description, completed, created_at, user_id) VALUES (?, ?, ?, ?, ?)",
        (todo.title, todo.description, todo.completed, now, user_id)
    )
    conn.commit()
    return cursor.lastrowid

# Endpointy API
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, conn = Depends(get_db)):
    """Tworzy nowego użytkownika."""
    user_id = create_user_db(conn, user)
    return {**user.dict(), "id": user_id}

@app.post("/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, user_id: int, conn = Depends(get_db)):
    """Tworzy nowe zadanie dla określonego użytkownika."""
    todo_id = create_todo_db(conn, todo, user_id)
    now = datetime.now().isoformat()
    return {**todo.dict(), "id": todo_id, "created_at": now}

@app.get("/todos/", response_model=List[Todo])
def read_todos(skip: int = 0, limit: int = 100, user_id: Optional[int] = None, conn = Depends(get_db)):
    """Pobiera listę wszystkich zadań lub zadania konkretnego użytkownika."""
    todos = get_todos(conn, skip, limit, user_id)
    return [dict(todo) for todo in todos]

@app.get("/")
def read_root():
    """Endpoint główny."""
    return {"message": "Witaj w prostej aplikacji Todo API!"}

# Uruchomienie aplikacji
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8000, reload=True) 