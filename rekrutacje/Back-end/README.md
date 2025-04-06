# Todo API

Proste API REST do zarządzania zadaniami (Todo) zbudowane przy użyciu FastAPI i SQLite.

## Wymagania

- Python 3.7+
- Zależności wymienione w pliku `requirements.txt`

## Instalacja

```bash
# Instalacja zależności
pip install -r requirements.txt
```

## Uruchomienie

```bash
# Uruchomienie serwera
python -m uvicorn app.main:app --reload
```

Serwer będzie dostępny pod adresem http://127.0.0.1:8000

## Dokumentacja API

Po uruchomieniu serwera, dokumentacja API jest dostępna pod adresem:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Dostępne endpointy

- `GET /` - Strona główna
- `GET /todos` - Pobierz wszystkie zadania
- `GET /todos/{todo_id}` - Pobierz szczegóły zadania
- `POST /todos` - Utwórz nowe zadanie
- `PUT /todos/{todo_id}` - Zaktualizuj zadanie
- `DELETE /todos/{todo_id}` - Usuń zadanie

## Przykład użycia

### Tworzenie nowego zadania

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/todos' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Przykładowe zadanie",
  "description": "Opis zadania",
  "completed": false
}'
``` 