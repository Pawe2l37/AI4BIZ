import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import os

# Import funkcji wizualizacyjnych
from visualize import (
    plot_confusion_matrix,
    plot_feature_importance,
    plot_learning_curves,
    plot_roc_curve,
    plot_precision_recall_curve,
    plot_decision_regions
)

def main():
    print("========== PROSTY MODEL KLASYFIKACJI ==========")
    
    # Wczytanie danych o raku piersi
    print("Używanie zbioru Breast Cancer Wisconsin")
    cancer = load_breast_cancer()
    X = cancer.data
    y = cancer.target
    feature_names = cancer.feature_names
    
    # Informacje o zbiorze danych
    print(f"\nInformacje o zbiorze danych:")
    print(f"Liczba próbek: {X.shape[0]}")
    print(f"Liczba cech: {X.shape[1]}")
    print(f"Klasy: {cancer.target_names}")
    print(f"Rozkład klas: {np.bincount(y)}")
    
    # Podział na zbiory treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nRozmiar zbioru treningowego: {X_train.shape}")
    print(f"Rozmiar zbioru testowego: {X_test.shape}")
    
    # Standaryzacja danych
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model regresji logistycznej
    print("\n--- MODEL REGRESJI LOGISTYCZNEJ ---")
    logreg = LogisticRegression(max_iter=1000, random_state=42)
    logreg.fit(X_train_scaled, y_train)
    
    # Predykcje
    y_pred_logreg = logreg.predict(X_test_scaled)
    y_prob_logreg = logreg.predict_proba(X_test_scaled)[:, 1]  # prawdopodobieństwa dla klasy pozytywnej
    
    # Ocena modelu
    accuracy_logreg = accuracy_score(y_test, y_pred_logreg)
    
    print(f"Dokładność (Accuracy): {accuracy_logreg:.4f}")
    print("\nRaport klasyfikacji:")
    print(classification_report(y_test, y_pred_logreg, target_names=['złośliwy', 'łagodny']))
    
    # Wydruk macierzy pomyłek w formie tekstowej
    cm = confusion_matrix(y_test, y_pred_logreg)
    print("\nMacierz pomyłek:")
    print("             Przewidziane")
    print("             Złośliwy  Łagodny")
    print(f"Rzeczywiste Złośliwy  {cm[0,0]:8d} {cm[0,1]:8d}")
    print(f"           Łagodny    {cm[1,0]:8d} {cm[1,1]:8d}")
    
    # Wizualizacja macierzy pomyłek dla regresji logistycznej
    plot_confusion_matrix(
        y_test, 
        y_pred_logreg, 
        class_names=['złośliwy', 'łagodny'],
        title='Macierz pomyłek - Regresja logistyczna'
    )
    
    # Wizualizacja krzywej ROC dla regresji logistycznej
    plot_roc_curve(
        y_test, 
        y_prob_logreg,
        title='Krzywa ROC - Regresja logistyczna'
    )
    
    # Wizualizacja krzywej Precision-Recall dla regresji logistycznej
    plot_precision_recall_curve(
        y_test, 
        y_prob_logreg,
        title='Krzywa Precision-Recall - Regresja logistyczna'
    )
    
    # Wyznaczanie krzywych uczenia dla regresji logistycznej
    plot_learning_curves(
        LogisticRegression(max_iter=1000, random_state=42),
        X_train_scaled, 
        y_train,
        title='Krzywe uczenia - Regresja logistyczna'
    )
    
    # Model Random Forest
    print("\n--- MODEL RANDOM FOREST ---")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train_scaled, y_train)
    
    # Predykcje
    y_pred_rf = rf.predict(X_test_scaled)
    y_prob_rf = rf.predict_proba(X_test_scaled)[:, 1]
    
    # Ocena modelu
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    
    print(f"Dokładność (Accuracy): {accuracy_rf:.4f}")
    print("\nRaport klasyfikacji:")
    print(classification_report(y_test, y_pred_rf, target_names=['złośliwy', 'łagodny']))
    
    # Wydruk macierzy pomyłek w formie tekstowej
    cm = confusion_matrix(y_test, y_pred_rf)
    print("\nMacierz pomyłek:")
    print("             Przewidziane")
    print("             Złośliwy  Łagodny")
    print(f"Rzeczywiste Złośliwy  {cm[0,0]:8d} {cm[0,1]:8d}")
    print(f"           Łagodny    {cm[1,0]:8d} {cm[1,1]:8d}")
    
    # Wizualizacja macierzy pomyłek dla Random Forest
    plot_confusion_matrix(
        y_test, 
        y_pred_rf, 
        class_names=['złośliwy', 'łagodny'],
        title='Macierz pomyłek - Random Forest'
    )
    
    # Wizualizacja krzywej ROC dla Random Forest
    plot_roc_curve(
        y_test, 
        y_prob_rf,
        title='Krzywa ROC - Random Forest'
    )
    
    # Wizualizacja krzywej Precision-Recall dla Random Forest
    plot_precision_recall_curve(
        y_test, 
        y_prob_rf,
        title='Krzywa Precision-Recall - Random Forest'
    )
    
    # Ważność cech dla Random Forest
    feature_importances = rf.feature_importances_
    indices = np.argsort(feature_importances)[::-1]
    
    # Top 10 najważniejszych cech dla modelu Random Forest
    print("\nTop 10 najważniejszych cech dla modelu Random Forest:")
    for i in range(min(10, X.shape[1])):
        print(f"{i+1}. {feature_names[indices[i]]}: {feature_importances[indices[i]]:.4f}")
    
    # Wizualizacja ważności cech
    plot_feature_importance(
        feature_names, 
        feature_importances,
        title='Ważność cech - Random Forest',
        top_n=15
    )
    
    # Wizualizacja krzywych uczenia dla Random Forest
    plot_learning_curves(
        RandomForestClassifier(n_estimators=100, random_state=42),
        X_train_scaled, 
        y_train,
        title='Krzywe uczenia - Random Forest'
    )
    
    # Wizualizacja regionów decyzyjnych dla dwóch najważniejszych cech
    try:
        plot_decision_regions(
            X_test_scaled, 
            y_test, 
            rf,
            title='Regiony decyzyjne - Random Forest',
            feature_indices=[indices[0], indices[1]]  # Dwie najważniejsze cechy
        )
    except Exception as e:
        print(f"Nie udało się utworzyć wykresu regionów decyzyjnych: {e}")
    
    # Podsumowanie wyników
    print("\n========== PODSUMOWANIE WYNIKÓW ==========")
    print(f"Regresja logistyczna - Dokładność: {accuracy_logreg:.4f}")
    print(f"Random Forest - Dokładność: {accuracy_rf:.4f}")
    
    # Interpretacja wyników
    print("\n========== INTERPRETACJA WYNIKÓW ==========")
    print("1. Dokładność (Accuracy) - procent poprawnie sklasyfikowanych próbek")
    print("2. Precision - dokładność pozytywnych identyfikacji (ile z przewidzianych jako łagodne faktycznie było łagodnych)")
    print("3. Recall - kompletność pozytywnych identyfikacji (jak dużo łagodnych próbek model prawidłowo zidentyfikował)")
    print("4. F1-score - średnia harmoniczna precision i recall")
    print("5. Macierz pomyłek - zestawienie przewidzianych vs. rzeczywistych klas")
    print("   - Wiersze: klasa rzeczywista")
    print("   - Kolumny: klasa przewidziana")
    print("6. Krzywa ROC - wykres True Positive Rate vs. False Positive Rate")
    print("   - AUC - pole pod krzywą ROC, wartość bliższa 1 oznacza lepszy model")
    print("7. Krzywa Precision-Recall - wykres Precision vs. Recall")
    print("8. Ważność cech - wskazuje, które cechy mają największy wpływ na decyzje modelu")
    
    print("\n========== PROPOZYCJE ULEPSZEŃ ==========")
    print("1. Hiperstrojenie parametrów modeli:")
    print("   - Zastosowanie GridSearchCV lub RandomizedSearchCV do znalezienia optymalnych parametrów")
    print("   - Dla regresji logistycznej: parametr C (regularyzacja), solver, penalty")
    print("   - Dla Random Forest: n_estimators, max_depth, min_samples_split, min_samples_leaf")
    
    print("\n2. Wypróbowanie innych modeli:")
    print("   - SVM (Support Vector Machine) - dobrze radzi sobie z danymi o wysokiej wymiarowości")
    print("   - XGBoost - implementacja gradient boosting, często osiąga najlepsze wyniki")
    print("   - Sieci neuronowe - dla złożonych zależności w danych")
    print("   - Naive Bayes - prosty model prawdopodobieństwa, często skuteczny dla mniejszych zbiorów danych")
    print("   - KNN (k-Nearest Neighbors) - klasyfikacja na podstawie podobieństwa do punktów treningowych")
    
    print("\n3. Inżynieria i selekcja cech:")
    print("   - Redukcja wymiarowości: PCA, t-SNE, UMAP")
    print("   - Wybór cech: SelectKBest, RFE (Recursive Feature Elimination)")
    print("   - Transformacje nieliniowe cech")
    print("   - Tworzenie nowych cech na podstawie domenowej znajomości problemu")
    
    print("\n4. Techniki uczenia:")
    print("   - Walidacja krzyżowa zamiast pojedynczego podziału")
    print("   - Stratyfikacja - zachowanie proporcji klas w zbiorach")
    print("   - Obsługa niezbalansowanych danych: SMOTE, upsampling, downsampling")
    print("   - Zespoły modeli: stacking, blending")
    
    print("\n5. Interpretacja modelu:")
    print("   - SHAP (SHapley Additive exPlanations) - dla wyjaśnienia decyzji modelu dla konkretnych przykładów")
    print("   - LIME (Local Interpretable Model-agnostic Explanations) - lokalna interpretacja")
    print("   - Partial Dependence Plots - wpływ zmian wartości cech na predykcje")
    
    print("\n6. Optymalizacja metryk:")
    print("   - Wybór odpowiedniej metryki dla domeny: precision, recall, F1, AUC")
    print("   - Dostosowanie progu decyzyjnego do kosztów błędów (fałszywie dodatnich vs. fałszywie ujemnych)")
    print("   - Kalibracja prawdopodobieństw modelu")

if __name__ == "__main__":
    # Utworzenie katalogu na wykresy, jeśli nie istnieje
    os.makedirs('wykresy', exist_ok=True)
    main() 