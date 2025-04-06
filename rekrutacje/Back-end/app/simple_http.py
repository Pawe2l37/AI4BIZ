import http.server
import socketserver
import json
import sqlite3
from urllib.parse import urlparse, parse_qs
import cgi
from datetime import datetime

# Konfiguracja portu
PORT = 8080

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

# Klasa obsługująca żądania HTTP
class TodoHandler(http.server.BaseHTTPRequestHandler):
    # Obsługa żądań GET
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Endpoint główny
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Witaj w Todo API!"}).encode('utf-8'))
            return
        
        # Endpoint do pobierania zadań
        elif path == '/todos':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Pobieranie zadań z bazy danych
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos ORDER BY id")
            todos = cursor.fetchall()
            conn.close()
            
            self.wfile.write(json.dumps(todos).encode('utf-8'))
            return
        
        # Endpoint do pobierania pojedynczego zadania
        elif path.startswith('/todos/'):
            todo_id = path.split('/')[-1]
            if not todo_id.isdigit():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Nieprawidłowe ID zadania"}).encode('utf-8'))
                return
                
            todo_id = int(todo_id)
            
            # Pobieranie zadania z bazy danych
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            todo = cursor.fetchone()
            conn.close()
            
            if todo:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(todo).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Zadanie nie znalezione"}).encode('utf-8'))
            return
        
        # Nieznany endpoint
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint nie znaleziony"}).encode('utf-8'))
    
    # Obsługa żądań POST
    def do_POST(self):
        if self.path == '/todos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                if not data.get('title'):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Tytuł zadania jest wymagany"}).encode('utf-8'))
                    return
                
                # Dodawanie zadania do bazy danych
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                created_at = datetime.now().isoformat()
                
                cursor.execute(
                    "INSERT INTO todos (title, description, completed, created_at) VALUES (?, ?, ?, ?)",
                    (data.get('title'), data.get('description', ''), data.get('completed', False), created_at)
                )
                conn.commit()
                
                todo_id = cursor.lastrowid
                cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
                new_todo = cursor.fetchone()
                conn.close()
                
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_todo).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Nieprawidłowy format JSON"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint nie znaleziony"}).encode('utf-8'))
    
    # Obsługa żądań PUT
    def do_PUT(self):
        if self.path.startswith('/todos/'):
            todo_id = self.path.split('/')[-1]
            if not todo_id.isdigit():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Nieprawidłowe ID zadania"}).encode('utf-8'))
                return
                
            todo_id = int(todo_id)
            
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(put_data.decode('utf-8'))
                
                # Aktualizacja zadania w bazie danych
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                
                # Sprawdzenie czy zadanie istnieje
                cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
                todo = cursor.fetchone()
                
                if not todo:
                    conn.close()
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Zadanie nie znalezione"}).encode('utf-8'))
                    return
                
                # Aktualizacja zadania
                title = data.get('title', todo['title'])
                description = data.get('description', todo['description'])
                completed = data.get('completed', todo['completed'])
                
                cursor.execute(
                    "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                    (title, description, completed, todo_id)
                )
                conn.commit()
                
                # Pobranie zaktualizowanego zadania
                cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
                updated_todo = cursor.fetchone()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(updated_todo).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Nieprawidłowy format JSON"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint nie znaleziony"}).encode('utf-8'))
    
    # Obsługa żądań DELETE
    def do_DELETE(self):
        if self.path.startswith('/todos/'):
            todo_id = self.path.split('/')[-1]
            if not todo_id.isdigit():
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Nieprawidłowe ID zadania"}).encode('utf-8'))
                return
                
            todo_id = int(todo_id)
            
            # Usunięcie zadania z bazy danych
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Sprawdzenie czy zadanie istnieje
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            todo = cursor.fetchone()
            
            if not todo:
                conn.close()
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Zadanie nie znalezione"}).encode('utf-8'))
                return
            
            # Usunięcie zadania
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            conn.close()
            
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint nie znaleziony"}).encode('utf-8'))

# Uruchomienie serwera
if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), TodoHandler) as httpd:
            print(f"Serwer uruchomiony na porcie {PORT}")
            print(f"Dostępny pod adresem: http://localhost:{PORT}/")
            print("Naciśnij CTRL+C aby zatrzymać serwer")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")
    except Exception as e:
        print(f"Wystąpił błąd: {e}") 