# Opis projektu: API Todo

## Cel projektu
Celem projektu jest stworzenie prostego API RESTful do zarządzania zadaniami (todo) dla wielu użytkowników. API pozwala na rejestrację użytkowników, dodawanie, aktualizację, usuwanie i pobieranie zadań.

## Technologie
- **Backend**: Python 3.x, Flask
- **Przechowywanie danych**: Plik JSON
- **Testowanie**: Biblioteka Requests

## Struktura projektu
- `flask_app.py` - Główny plik aplikacji zawierający endpointy API
- `test_flask.py` - Skrypt do testowania API
- `db.json` - Plik przechowujący dane (tworzony automatycznie)
- `README.md` - Instrukcja użycia API
- `project_description.md` - Opis projektu (ten plik)

## Funkcjonalności API

### Zarządzanie użytkownikami
- Rejestracja nowych użytkowników
- Pobieranie listy wszystkich użytkowników
- Pobieranie konkretnego użytkownika według ID

### Zarządzanie zadaniami
- Tworzenie nowych zadań dla użytkownika
- Pobieranie wszystkich zadań użytkownika
- Pobieranie konkretnego zadania według ID
- Aktualizacja istniejących zadań (tytuł, opis, status ukończenia)
- Usuwanie zadań

## Struktura danych

### Użytkownik
```json
{
  "id": 1,
  "username": "przykładowy_użytkownik",
  "created_at": "2023-07-25T14:30:00.000Z"
}
```

### Zadanie
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Przykładowe zadanie",
  "description": "Opis przykładowego zadania",
  "completed": false,
  "created_at": "2023-07-25T14:35:00.000Z",
  "updated_at": "2023-07-25T15:00:00.000Z"
}
```

## Endpointy API

### Użytkownicy
- `GET /users` - Lista wszystkich użytkowników
- `GET /users/<id>` - Szczegóły użytkownika
- `POST /users` - Rejestracja użytkownika (wymagane pole: username)

### Zadania
- `GET /users/<user_id>/tasks` - Lista zadań użytkownika
- `POST /users/<user_id>/tasks` - Dodanie zadania dla użytkownika (wymagane pole: title)
- `GET /tasks/<task_id>` - Szczegóły zadania
- `PUT /tasks/<task_id>` - Aktualizacja zadania
- `DELETE /tasks/<task_id>` - Usunięcie zadania

## Rozszerzenia projektu (potencjalne)
- Dodanie uwierzytelniania (JWT)
- Obsługa kategorii zadań
- Dodanie priorytetów zadań
- Implementacja terminu wykonania zadań
- Migracja do bazy danych (np. SQLite, PostgreSQL)
- Dodanie dokumentacji Swagger
- Rozszerzone filtrowanie i sortowanie zadań 