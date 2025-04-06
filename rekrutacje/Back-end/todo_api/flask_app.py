import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
import os

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Ścieżka do pliku bazy danych
DB_FILE = "db.json"

# Funkcja do ładowania danych z pliku JSON
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"users": [], "tasks": []}
    else:
        return {"users": [], "tasks": []}

# Funkcja do zapisywania danych do pliku JSON
def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Główna strona
@app.route('/')
def index():
    return jsonify({"message": "Witaj w API Todo!"})

# Endpoint do rejestracji użytkownika
@app.route('/users', methods=['POST'])
def add_user():
    data = load_data()
    request_data = request.get_json()
    
    if not request_data or 'username' not in request_data:
        return jsonify({"error": "Brak wymaganego pola 'username'"}), 400
    
    username = request_data['username']
    
    # Sprawdzamy, czy użytkownik już istnieje
    for user in data["users"]:
        if user["username"] == username:
            return jsonify({"error": "Użytkownik o podanej nazwie już istnieje"}), 400
    
    # Tworzymy nowego użytkownika
    user_id = len(data["users"]) + 1
    new_user = {
        "id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat()
    }
    
    data["users"].append(new_user)
    save_data(data)
    
    return jsonify(new_user), 201

# Endpoint do pobierania listy użytkowników
@app.route('/users', methods=['GET'])
def get_users():
    data = load_data()
    return jsonify(data["users"])

# Endpoint do pobierania konkretnego użytkownika
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = load_data()
    for user in data["users"]:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "Użytkownik nie znaleziony"}), 404

# Endpoint do dodawania zadania
@app.route('/users/<int:user_id>/tasks', methods=['POST'])
def add_task(user_id):
    data = load_data()
    request_data = request.get_json()
    
    # Sprawdzamy, czy użytkownik istnieje
    user_exists = False
    for user in data["users"]:
        if user["id"] == user_id:
            user_exists = True
            break
            
    if not user_exists:
        return jsonify({"error": "Użytkownik nie znaleziony"}), 404
        
    if not request_data or 'title' not in request_data:
        return jsonify({"error": "Brak wymaganego pola 'title'"}), 400
    
    # Tworzymy nowe zadanie
    task_id = len(data["tasks"]) + 1
    new_task = {
        "id": task_id,
        "user_id": user_id,
        "title": request_data["title"],
        "description": request_data.get("description", ""),
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    data["tasks"].append(new_task)
    save_data(data)
    
    return jsonify(new_task), 201

# Endpoint do pobierania zadań użytkownika
@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    data = load_data()
    user_tasks = [task for task in data["tasks"] if task["user_id"] == user_id]
    return jsonify(user_tasks)

# Endpoint do pobierania konkretnego zadania
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    data = load_data()
    for task in data["tasks"]:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "Zadanie nie znalezione"}), 404

# Endpoint do aktualizacji zadania
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = load_data()
    request_data = request.get_json()
    
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            # Aktualizujemy dane zadania
            data["tasks"][i]["title"] = request_data.get("title", task["title"])
            data["tasks"][i]["description"] = request_data.get("description", task["description"])
            data["tasks"][i]["completed"] = request_data.get("completed", task["completed"])
            data["tasks"][i]["updated_at"] = datetime.now().isoformat()
            
            save_data(data)
            return jsonify(data["tasks"][i])
            
    return jsonify({"error": "Zadanie nie znalezione"}), 404

# Endpoint do usuwania zadania
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    data = load_data()
    
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            deleted_task = data["tasks"].pop(i)
            save_data(data)
            return jsonify({"message": f"Zadanie '{deleted_task['title']}' zostało usunięte"})
            
    return jsonify({"error": "Zadanie nie znalezione"}), 404

if __name__ == '__main__':
    # Upewniamy się, że plik bazy danych istnieje
    if not os.path.exists(DB_FILE):
        save_data({"users": [], "tasks": []})
    app.run(debug=True) 