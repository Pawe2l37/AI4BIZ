from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
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

# Funkcja inicjująca bazę danych
def init_db():
    print(f"Inicjalizacja bazy danych: {DB_PATH}")
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
    print("Baza danych zainicjalizowana!")

# Inicjalizacja bazy danych
init_db()

# Endpoint powitalny
@app.get("/")
def read_root():
    return {"message": "Witaj w Todo API"}

# Endpoints dla zadań
@app.get("/todos")
def read_todos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY id")
    todos = cursor.fetchall()
    conn.close()
    return [dict(todo) for todo in todos]

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    conn.close()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    return dict(todo)

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO todos (title, description, completed, created_at) VALUES (?, ?, ?, ?)",
        (todo.title, todo.description, todo.completed, created_at)
    )
    conn.commit()
    
    todo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    new_todo = cursor.fetchone()
    conn.close()
    
    return dict(new_todo)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    
    if db_todo is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    
    cursor.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (todo.title, todo.description, todo.completed, todo_id)
    )
    conn.commit()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    updated_todo = cursor.fetchone()
    conn.close()
    
    return dict(updated_todo)

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    
    if db_todo is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    return None

# Uruchomienie aplikacji z Hypercorn
if __name__ == "__main__":
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    
    print("Uruchamianie aplikacji za pomocą Hypercorn na http://127.0.0.1:8000/")
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    
    asyncio.run(serve(app, config)) 