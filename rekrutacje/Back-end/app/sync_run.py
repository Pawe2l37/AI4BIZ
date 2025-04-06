import sys
import os

print("Sprawdzanie środowiska Python...")
print(f"Wersja Python: {sys.version}")
print(f"Ścieżka interpretera: {sys.executable}")

try:
    import flask
    print(f"Flask zainstalowany: wersja {flask.__version__}")
except ImportError:
    print("Flask nie jest zainstalowany")

print("\nPróba uruchomienia minimalnego serwera Flask...")
try:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello World!"
    
    print("Tworzenie aplikacji Flask powiodło się.")
    print("Uruchamianie serwera na http://127.0.0.1:5000/")
    print("Wciśnij CTRL+C, aby zatrzymać serwer.")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
except Exception as e:
    print(f"Błąd przy uruchamianiu Flask: {e}") 