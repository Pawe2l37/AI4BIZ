# Mini-aplikacja React - Lista Użytkowników

## Opis projektu
Prosta aplikacja React, która pobiera dane użytkowników z JSONPlaceholder API i wyświetla je w formie listy kart. Aplikacja umożliwia również filtrowanie użytkowników poprzez wyszukiwanie.

## Funkcjonalności
- Pobieranie danych użytkowników z JSONPlaceholder API
- Wyświetlanie listy użytkowników w formie kart
- Wyszukiwanie użytkowników po nazwie, nazwie użytkownika lub adresie email
- Responsywny układ strony dzięki Bootstrap
- Animacje kart przy najechaniu
- Obsługa błędów i stanów ładowania

## Technologie
- React
- Bootstrap (stylizacja)
- Bootstrap Icons (ikony)
- Axios (pobieranie danych z API)

## Struktura projektu
- `src/components/` - folder zawierający komponenty React
  - `UserCard.jsx` - komponent karty pojedynczego użytkownika
  - `UserList.jsx` - komponent listy użytkowników z logiką filtrowania
  - `SearchBar.jsx` - komponent paska wyszukiwania
- `src/services/` - folder zawierający usługi
  - `api.js` - serwis do komunikacji z API

## Uruchomienie projektu
1. Zainstaluj zależności: `npm install`
2. Uruchom aplikację: `npm start`
3. Otwórz przeglądarkę na adresie: `http://localhost:3000` 