from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import json

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

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

# Pomocnicza funkcja do konwersji obiektu row na słownik
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Endpoint powitalny
@app.route('/')
def read_root():
    return jsonify({"message": "Witaj w Todo API"})

# Pobieranie wszystkich zadań
@app.route('/todos', methods=['GET'])
def read_todos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos ORDER BY id")
    todos = cursor.fetchall()
    conn.close()
    return jsonify(todos)

# Pobieranie pojedynczego zadania
@app.route('/todos/<int:todo_id>', methods=['GET'])
def read_todo(todo_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    conn.close()
    
    if todo is None:
        return jsonify({"detail": "Zadanie nie znalezione"}), 404
    return jsonify(todo)

# Tworzenie nowego zadania
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"detail": "Brak tytułu zadania"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    
    title = data.get('title')
    description = data.get('description', '')
    completed = data.get('completed', False)
    
    cursor.execute(
        "INSERT INTO todos (title, description, completed, created_at) VALUES (?, ?, ?, ?)",
        (title, description, completed, created_at)
    )
    conn.commit()
    
    todo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    new_todo = cursor.fetchone()
    conn.close()
    
    return jsonify(new_todo), 201

# Aktualizacja zadania
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({"detail": "Brak danych do aktualizacji"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    
    if db_todo is None:
        conn.close()
        return jsonify({"detail": "Zadanie nie znalezione"}), 404
    
    title = data.get('title', db_todo['title'])
    description = data.get('description', db_todo['description'])
    completed = data.get('completed', db_todo['completed'])
    
    cursor.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (title, description, completed, todo_id)
    )
    conn.commit()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    updated_todo = cursor.fetchone()
    conn.close()
    
    return jsonify(updated_todo)

# Usuwanie zadania
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    db_todo = cursor.fetchone()
    
    if db_todo is None:
        conn.close()
        return jsonify({"detail": "Zadanie nie znalezione"}), 404
    
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    return "", 204

# Uruchomienie aplikacji
if __name__ == "__main__":
    print("Uruchamianie Flask API na http://127.0.0.1:5000/")
    app.run(debug=True) 