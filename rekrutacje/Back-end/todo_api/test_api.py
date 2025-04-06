import requests
import json

# Adres bazowy API
BASE_URL = "http://localhost:8000"

def test_api():
    """Funkcja testująca podstawowe operacje API."""
    print("Rozpoczynam testy API...")
    
    # 1. Sprawdzenie głównego endpointu
    print("\n1. Test głównego endpointu:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Odpowiedź: {response.json()}")
    
    # 2. Tworzenie nowego użytkownika
    print("\n2. Tworzenie nowego użytkownika:")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "haslo123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Odpowiedź: {response.json()}")
    
    # Pobieramy ID utworzonego użytkownika
    user_id = response.json().get("id")
    
    # 3. Tworzenie nowego zadania
    print("\n3. Tworzenie nowego zadania:")
    todo_data = {
        "title": "Przykładowe zadanie",
        "description": "Opis przykładowego zadania",
        "completed": False
    }
    response = requests.post(f"{BASE_URL}/todos/?user_id={user_id}", json=todo_data)
    print(f"Status: {response.status_code}")
    print(f"Odpowiedź: {response.json()}")
    
    # 4. Pobieranie listy zadań
    print("\n4. Pobieranie wszystkich zadań:")
    response = requests.get(f"{BASE_URL}/todos/")
    print(f"Status: {response.status_code}")
    print(f"Odpowiedź: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 5. Pobieranie zadań konkretnego użytkownika
    print("\n5. Pobieranie zadań dla użytkownika:")
    response = requests.get(f"{BASE_URL}/todos/?user_id={user_id}")
    print(f"Status: {response.status_code}")
    print(f"Odpowiedź: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    print("\nTesty zakończone.")

if __name__ == "__main__":
    test_api() 