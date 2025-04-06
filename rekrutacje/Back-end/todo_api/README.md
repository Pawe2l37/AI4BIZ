# API Todo

Prosta aplikacja API do zarządzania zadaniami (todo), napisana w języku Python z wykorzystaniem Flask.

## Funkcjonalności

- Rejestracja użytkowników
- Dodawanie, pobieranie, aktualizacja i usuwanie zadań
- Filtrowanie zadań według użytkownika
- Przechowywanie danych w pliku JSON

## Wymagania

- Python 3.6+
- Flask
- Requests (do testów)

## Instalacja

1. Sklonuj repozytorium lub utwórz pliki zgodnie z instrukcją
2. Zainstaluj wymagane zależności:

```bash
pip install flask requests
```

## Uruchomienie

```bash
python flask_app.py
```

Aplikacja będzie dostępna pod adresem http://localhost:5000/

## Testowanie

Aby przetestować API, uruchom skrypt testowy:

```bash
python test_flask.py
```

## Endpoints API

### Użytkownicy

- `GET /users` - Pobierz wszystkich użytkowników
- `GET /users/<id>` - Pobierz użytkownika o podanym ID
- `POST /users` - Utwórz nowego użytkownika (wymaga `username` w ciele żądania)

### Zadania

- `GET /users/<user_id>/tasks` - Pobierz wszystkie zadania użytkownika
- `POST /users/<user_id>/tasks` - Utwórz nowe zadanie dla użytkownika (wymaga `title` w ciele żądania)
- `GET /tasks/<task_id>` - Pobierz szczegóły zadania
- `PUT /tasks/<task_id>` - Zaktualizuj zadanie
- `DELETE /tasks/<task_id>` - Usuń zadanie

## Przykłady użycia

### Tworzenie użytkownika

```bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"username": "testuser"}'
```

### Tworzenie zadania

```bash
curl -X POST http://localhost:5000/users/1/tasks -H "Content-Type: application/json" -d '{"title": "Zadanie testowe", "description": "Opis zadania"}'
```

### Pobieranie zadań użytkownika

```bash
curl http://localhost:5000/users/1/tasks
```

### Aktualizacja zadania

```bash
curl -X PUT http://localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"title": "Zaktualizowane zadanie", "completed": true}'
```

### Usuwanie zadania

```bash
curl -X DELETE http://localhost:5000/tasks/1
```