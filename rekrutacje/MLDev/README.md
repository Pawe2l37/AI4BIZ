# Projekt uczenia maszynowego

## Opis
Projekt demonstruje zastosowanie prostych modeli uczenia maszynowego do zadań regresji i klasyfikacji przy użyciu scikit-learn. Projekt zawiera:
- Model regresji liniowej i Random Forest na zbiorze California Housing
- Model klasyfikacji (regresja logistyczna i Random Forest) na zbiorze Breast Cancer Wisconsin
- Wizualizacje wyników w postaci wykresów

## Wymagania
Projekt korzysta z następujących bibliotek:
- Python 3.6+
- scikit-learn
- numpy
- pandas
- matplotlib
- seaborn

## Instalacja
Aby zainstalować wymagane biblioteki, wykonaj:
```
pip install scikit-learn numpy pandas matplotlib seaborn
```

## Struktura projektu
- `model_ml.py` - główny skrypt zawierający implementacje modeli
- `visualize.py` - funkcje do wizualizacji wyników
- `project_description.md` - opis założeń projektu
- `wykresy/` - katalog z wygenerowanymi wykresami

## Uruchomienie
Aby uruchomić projekt, wykonaj:
```
python model_ml.py
```

Po wykonaniu skryptu, w konsoli zostaną wyświetlone wyniki analiz, a w katalogu `wykresy/` pojawią się wizualizacje wyników.

## Interpretacja wyników
Po uruchomieniu skryptu:
1. Ocena modeli regresji będzie mierzona przy użyciu MSE (Mean Squared Error) oraz R² (współczynnik determinacji)
2. Ocena modeli klasyfikacji będzie mierzona przy użyciu dokładności (accuracy), precyzji (precision), czułości (recall) oraz miary F1

## Możliwe ulepszenia
Projekt można ulepszyć poprzez:
1. Hiperstrojenie parametrów modeli (np. GridSearchCV)
2. Wypróbowanie innych modeli (SVM, XGBoost, sieci neuronowe)
3. Inżynierię cech i selekcję najważniejszych zmiennych
4. Zastosowanie technik redukcji wymiarowości (np. PCA)
5. Walidację krzyżową zamiast pojedynczego podziału na zbiory 