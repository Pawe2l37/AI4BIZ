import subprocess
import webbrowser
import time
import os

print("Uruchamianie serwera FastAPI...")

# Uruchom polecenie w osobnym procesie
process = subprocess.Popen(["py", "-m", "uvicorn", "app.main:app", "--port", "8005"])

# Poczekaj 3 sekundy na uruchomienie serwera
print("Czekam 3 sekundy na start serwera...")
time.sleep(3)

# Otwórz przeglądarkę
print("Otwieram przeglądarkę...")
webbrowser.open("http://127.0.0.1:8005")

print("Naciśnij Ctrl+C, aby zatrzymać serwer")
try:
    # Utrzymuj skrypt działającym
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Zatrzymaj serwer po naciśnięciu Ctrl+C
    print("Zatrzymuję serwer...")
    process.terminate() 