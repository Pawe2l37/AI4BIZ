import requests
import json
import time

# Adres bazowy API
BASE_URL = "http://localhost:5000"

def test_api():
    """Funkcja testująca podstawowe operacje API Flask."""
    print("Testowanie API Todo...")
    
    # Sprawdzanie głównej strony
    print("\n1. Sprawdzanie głównej strony")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Statuscode: {response.status_code}")
        print(f"Odpowiedź: {response.json()}")
    except Exception as e:
        print(f"Błąd: {e}")
        return
    
    # Dodawanie użytkownika
    print("\n2. Dodawanie użytkownika")
    try:
        response = requests.post(
            f"{BASE_URL}/users",
            json={"username": f"testowy_user_{int(time.time())}"}
        )
        print(f"Statuscode: {response.status_code}")
        print(f"Odpowiedź: {response.json()}")
        
        if response.status_code == 201:
            user_id = response.json()["id"]
            print(f"Utworzono użytkownika o ID: {user_id}")
        else:
            print("Nie udało się utworzyć użytkownika")
            return
    except Exception as e:
        print(f"Błąd: {e}")
        return
    
    # Pobieranie listy użytkowników
    print("\n3. Pobieranie listy użytkowników")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Statuscode: {response.status_code}")
        print(f"Liczba użytkowników: {len(response.json())}")
    except Exception as e:
        print(f"Błąd: {e}")
    
    # Dodawanie zadań dla użytkownika
    print(f"\n4. Dodawanie zadań dla użytkownika {user_id}")
    task_ids = []
    
    for i in range(3):
        try:
            task_data = {
                "title": f"Zadanie testowe {i+1}",
                "description": f"Opis zadania testowego {i+1}"
            }
            
            response = requests.post(
                f"{BASE_URL}/users/{user_id}/tasks",
                json=task_data
            )
            
            print(f"Statuscode: {response.status_code}")
            if response.status_code == 201:
                task_id = response.json()["id"]
                task_ids.append(task_id)
                print(f"Utworzono zadanie o ID: {task_id}")
            else:
                print(f"Nie udało się utworzyć zadania: {response.json()}")
        except Exception as e:
            print(f"Błąd: {e}")
    
    # Pobieranie zadań użytkownika
    print(f"\n5. Pobieranie zadań użytkownika {user_id}")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}/tasks")
        print(f"Statuscode: {response.status_code}")
        print(f"Liczba zadań: {len(response.json())}")
        for task in response.json():
            print(f"- {task['title']}")
    except Exception as e:
        print(f"Błąd: {e}")
    
    # Aktualizacja zadania
    if task_ids:
        print(f"\n6. Aktualizacja zadania {task_ids[0]}")
        try:
            task_data = {
                "title": "Zaktualizowane zadanie",
                "completed": True
            }
            
            response = requests.put(
                f"{BASE_URL}/tasks/{task_ids[0]}",
                json=task_data
            )
            
            print(f"Statuscode: {response.status_code}")
            if response.status_code == 200:
                print(f"Zaktualizowano zadanie: {response.json()['title']}")
                print(f"Status ukończenia: {response.json()['completed']}")
            else:
                print(f"Nie udało się zaktualizować zadania: {response.json()}")
        except Exception as e:
            print(f"Błąd: {e}")
    
    # Usuwanie zadania
    if len(task_ids) > 1:
        print(f"\n7. Usuwanie zadania {task_ids[1]}")
        try:
            response = requests.delete(f"{BASE_URL}/tasks/{task_ids[1]}")
            
            print(f"Statuscode: {response.status_code}")
            if response.status_code == 200:
                print(f"Odpowiedź: {response.json()}")
            else:
                print(f"Nie udało się usunąć zadania: {response.json()}")
        except Exception as e:
            print(f"Błąd: {e}")
    
    print("\nTesty API zakończone!")

if __name__ == "__main__":
    test_api() 