import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import os

# Import funkcji wizualizacyjnych
from visualize import (
    plot_regression_results,
    plot_feature_importance,
    plot_confusion_matrix,
    plot_learning_curves
)

def main():
    # Tworzenie katalogu na wykresy, jeśli nie istnieje
    os.makedirs('wykresy', exist_ok=True)
    
    print("========== PROJEKT UCZENIA MASZYNOWEGO ==========")
    
    # ========== Model regresji ==========
    print("\n--- MODEL REGRESJI ---")
    # Wczytanie danych
    try:
        from sklearn.datasets import fetch_california_housing
        print("Używanie zbioru California Housing")
        housing = fetch_california_housing()
        X_reg = housing.data
        y_reg = housing.target
        feature_names_reg = housing.feature_names
    except:
        # Fallback - symulujemy dane jeśli zbiór niedostępny
        print("Generowanie syntetycznych danych regresji")
        np.random.seed(42)
        X_reg = np.random.rand(500, 5)
        y_reg = 2 + 3*X_reg[:, 0] + 4*X_reg[:, 1] - 2*X_reg[:, 2] + np.random.randn(500)*0.5
        feature_names_reg = [f'cecha_{i}' for i in range(X_reg.shape[1])]
    
    # Podział na zbiory treningowy i testowy
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )
    
    # Standaryzacja danych
    scaler_reg = StandardScaler()
    X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
    X_test_reg_scaled = scaler_reg.transform(X_test_reg)
    
    # Model regresji liniowej
    print("\nModel regresji liniowej:")
    lr = LinearRegression()
    lr.fit(X_train_reg_scaled, y_train_reg)
    
    # Predykcje
    y_pred_lr = lr.predict(X_test_reg_scaled)
    
    # Ocena modelu
    mse_lr = mean_squared_error(y_test_reg, y_pred_lr)
    r2_lr = r2_score(y_test_reg, y_pred_lr)
    
    print(f"Mean Squared Error: {mse_lr:.4f}")
    print(f"R² Score: {r2_lr:.4f}")
    
    # Wydruk wag modelu
    print("\nWagi modelu regresji liniowej:")
    for feat, coef in zip(feature_names_reg, lr.coef_):
        print(f"{feat}: {coef:.4f}")
    
    # Wizualizacja wyników regresji liniowej
    plot_regression_results(
        y_test_reg, 
        y_pred_lr, 
        title='Regresja Liniowa: Porównanie wartości rzeczywistych i przewidywanych'
    )
    
    # Model RandomForest dla regresji
    print("\nModel Random Forest dla regresji:")
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_reg.fit(X_train_reg_scaled, y_train_reg)
    
    # Predykcje
    y_pred_rf_reg = rf_reg.predict(X_test_reg_scaled)
    
    # Ocena modelu
    mse_rf_reg = mean_squared_error(y_test_reg, y_pred_rf_reg)
    r2_rf_reg = r2_score(y_test_reg, y_pred_rf_reg)
    
    print(f"Mean Squared Error: {mse_rf_reg:.4f}")
    print(f"R² Score: {r2_rf_reg:.4f}")
    
    # Ważność cech
    print("\nWażność cech w modelu Random Forest:")
    for feat, imp in zip(feature_names_reg, rf_reg.feature_importances_):
        print(f"{feat}: {imp:.4f}")
    
    # Wizualizacja ważności cech dla modelu RandomForest regresji
    plot_feature_importance(
        np.array(feature_names_reg), 
        rf_reg.feature_importances_,
        title='Ważność cech w modelu Random Forest dla regresji'
    )
    
    # Krzywe uczenia dla regresji
    train_sizes_reg, train_scores_reg, test_scores_reg = learning_curve(
        LinearRegression(), 
        X_train_reg_scaled, 
        y_train_reg,
        train_sizes=np.linspace(0.1, 1.0, 5),
        cv=5,
        scoring='neg_mean_squared_error'
    )
    
    # Wizualizacja krzywych uczenia dla regresji
    plot_learning_curves(
        -train_scores_reg,  # Negujemy, bo używamy neg_mean_squared_error
        -test_scores_reg, 
        train_sizes_reg,
        metric_name='Mean Squared Error'
    )
    
    # ========== Model klasyfikacji ==========
    print("\n\n--- MODEL KLASYFIKACJI ---")
    # Wczytanie danych
    print("Używanie zbioru Breast Cancer Wisconsin")
    cancer = load_breast_cancer()
    X_clf = cancer.data
    y_clf = cancer.target
    feature_names_clf = cancer.feature_names
    
    # Podział na zbiory treningowy i testowy
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42
    )
    
    # Standaryzacja danych
    scaler_clf = StandardScaler()
    X_train_clf_scaled = scaler_clf.fit_transform(X_train_clf)
    X_test_clf_scaled = scaler_clf.transform(X_test_clf)
    
    # Model regresji logistycznej
    print("\nModel regresji logistycznej:")
    logreg = LogisticRegression(max_iter=1000, random_state=42)
    logreg.fit(X_train_clf_scaled, y_train_clf)
    
    # Predykcje
    y_pred_logreg = logreg.predict(X_test_clf_scaled)
    
    # Ocena modelu
    accuracy_logreg = accuracy_score(y_test_clf, y_pred_logreg)
    
    print(f"Accuracy: {accuracy_logreg:.4f}")
    print("\nRaport klasyfikacji:")
    print(classification_report(y_test_clf, y_pred_logreg))
    
    # Wizualizacja macierzy pomyłek dla regresji logistycznej
    plot_confusion_matrix(
        y_test_clf, 
        y_pred_logreg,
        class_names=['złośliwy', 'łagodny'],
        title='Macierz pomyłek dla regresji logistycznej'
    )
    
    # Model RandomForest dla klasyfikacji
    print("\nModel Random Forest dla klasyfikacji:")
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(X_train_clf_scaled, y_train_clf)
    
    # Predykcje
    y_pred_rf_clf = rf_clf.predict(X_test_clf_scaled)
    
    # Ocena modelu
    accuracy_rf_clf = accuracy_score(y_test_clf, y_pred_rf_clf)
    
    print(f"Accuracy: {accuracy_rf_clf:.4f}")
    print("\nRaport klasyfikacji:")
    print(classification_report(y_test_clf, y_pred_rf_clf))
    
    # Wizualizacja macierzy pomyłek dla Random Forest
    plot_confusion_matrix(
        y_test_clf, 
        y_pred_rf_clf,
        class_names=['złośliwy', 'łagodny'],
        title='Macierz pomyłek dla modelu Random Forest'
    )
    
    # Ważność cech
    print("\nWażność cech w modelu Random Forest:")
    for feat, imp in zip(feature_names_clf, rf_clf.feature_importances_):
        print(f"{feat}: {imp:.4f}")
        
    # Wizualizacja ważności cech dla modelu RandomForest klasyfikacji
    plot_feature_importance(
        np.array(feature_names_clf), 
        rf_clf.feature_importances_,
        title='Ważność cech w modelu Random Forest dla klasyfikacji'
    )
    
    # Krzywe uczenia dla klasyfikacji
    train_sizes_clf, train_scores_clf, test_scores_clf = learning_curve(
        LogisticRegression(max_iter=1000, random_state=42), 
        X_train_clf_scaled, 
        y_train_clf,
        train_sizes=np.linspace(0.1, 1.0, 5),
        cv=5,
        scoring='accuracy'
    )
    
    # Wizualizacja krzywych uczenia dla klasyfikacji
    plot_learning_curves(
        train_scores_clf, 
        test_scores_clf, 
        train_sizes_clf,
        metric_name='Accuracy'
    )
    
    # Podsumowanie wyników
    print("\n========== PODSUMOWANIE WYNIKÓW ==========")
    print("\nRegresja:")
    print(f"Regresja liniowa - MSE: {mse_lr:.4f}, R²: {r2_lr:.4f}")
    print(f"Random Forest - MSE: {mse_rf_reg:.4f}, R²: {r2_rf_reg:.4f}")
    
    print("\nKlasyfikacja:")
    print(f"Regresja logistyczna - Accuracy: {accuracy_logreg:.4f}")
    print(f"Random Forest - Accuracy: {accuracy_rf_clf:.4f}")
    
    print("\n========== PROPOZYCJE ULEPSZEŃ ==========")
    print("1. Hiperstrojenie parametrów modeli (np. GridSearchCV)")
    print("2. Wypróbowanie innych modeli (SVM, XGBoost, sieci neuronowe)")
    print("3. Inżynieria cech i selekcja najważniejszych zmiennych")
    print("4. Zastosowanie technik redukcji wymiarowości (np. PCA)")
    print("5. Walidacja krzyżowa zamiast pojedynczego podziału na zbiory")

if __name__ == "__main__":
    main() 