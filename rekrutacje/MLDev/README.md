# Prosty projekt klasyfikacji danych medycznych

## Opis
Projekt demonstruje zastosowanie modeli klasyfikacji do analizy danych medycznych dotyczących raka piersi.
Używamy dwóch modeli klasyfikacji:
- Regresja logistyczna
- Random Forest

Dane pochodzą ze zbioru Breast Cancer Wisconsin z pakietu scikit-learn.

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
- `visualize.py` - funkcje do wizualizacji wyników modeli
- `project_description.md` - opis założeń projektu
- `wykresy/` - katalog z wygenerowanymi wykresami

## Uruchomienie
Aby uruchomić projekt, wykonaj:
```
python model_ml.py
```

Po wykonaniu skryptu, w konsoli zostaną wyświetlone wyniki analiz, a w katalogu `wykresy/` pojawią się wizualizacje wyników.

## Opis zbioru danych
Zbiór danych Breast Cancer Wisconsin zawiera cechy obliczone na podstawie cyfrowego obrazu biopsji cienkoigłowej guza piersi, opisujące charakterystykę jąder komórkowych widocznych na obrazie.

Klasy:
- 0: złośliwy (malignant)
- 1: łagodny (benign)

## Interpretacja wyników
1. **Dokładność (Accuracy)** - procent poprawnie sklasyfikowanych próbek
2. **Precision** - dokładność pozytywnych identyfikacji (ile z przewidzianych jako łagodne faktycznie było łagodnych)
3. **Recall** - kompletność pozytywnych identyfikacji (jak dużo łagodnych próbek model prawidłowo zidentyfikował)
4. **F1-score** - średnia harmoniczna precision i recall
5. **Macierz pomyłek** - zestawienie przewidzianych vs. rzeczywistych klas:
   - Wiersze: klasa rzeczywista
   - Kolumny: klasa przewidziana
6. **Krzywa ROC** - wykres True Positive Rate vs. False Positive Rate
   - AUC - pole pod krzywą ROC, wartość bliższa 1 oznacza lepszy model
7. **Krzywa Precision-Recall** - wykres zależności między precyzją a czułością
8. **Ważność cech** - wskazuje, które cechy mają największy wpływ na decyzje modelu

## Wygenerowane wizualizacje
- Macierz pomyłek dla obu modeli
- Krzywe ROC dla obu modeli
- Krzywe Precision-Recall dla obu modeli
- Ważność cech dla modelu Random Forest
- Krzywe uczenia dla obu modeli
- Regiony decyzyjne dla najważniejszych cech

## Propozycje ulepszeń
### 1. Hiperstrojenie parametrów modeli:
- Zastosowanie GridSearchCV lub RandomizedSearchCV do znalezienia optymalnych parametrów
- Dla regresji logistycznej: parametr C (regularyzacja), solver, penalty
- Dla Random Forest: n_estimators, max_depth, min_samples_split, min_samples_leaf

### 2. Wypróbowanie innych modeli:
- SVM (Support Vector Machine) - dobrze radzi sobie z danymi o wysokiej wymiarowości
- XGBoost - implementacja gradient boosting, często osiąga najlepsze wyniki
- Sieci neuronowe - dla złożonych zależności w danych
- Naive Bayes - prosty model prawdopodobieństwa, często skuteczny dla mniejszych zbiorów danych
- KNN (k-Nearest Neighbors) - klasyfikacja na podstawie podobieństwa do punktów treningowych

### 3. Inżynieria i selekcja cech:
- Redukcja wymiarowości: PCA, t-SNE, UMAP
- Wybór cech: SelectKBest, RFE (Recursive Feature Elimination)
- Transformacje nieliniowe cech
- Tworzenie nowych cech na podstawie domenowej znajomości problemu

### 4. Techniki uczenia:
- Walidacja krzyżowa zamiast pojedynczego podziału
- Stratyfikacja - zachowanie proporcji klas w zbiorach
- Obsługa niezbalansowanych danych: SMOTE, upsampling, downsampling
- Zespoły modeli: stacking, blending

### 5. Interpretacja modelu:
- SHAP (SHapley Additive exPlanations) - dla wyjaśnienia decyzji modelu dla konkretnych przykładów
- LIME (Local Interpretable Model-agnostic Explanations) - lokalna interpretacja
- Partial Dependence Plots - wpływ zmian wartości cech na predykcje

### 6. Optymalizacja metryk:
- Wybór odpowiedniej metryki dla domeny: precision, recall, F1, AUC
- Dostosowanie progu decyzyjnego do kosztów błędów (fałszywie dodatnich vs. fałszywie ujemnych)
- Kalibracja prawdopodobieństw modelu 