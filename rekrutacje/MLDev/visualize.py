import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import os

def plot_regression_results(y_true, y_pred, title='Porównanie wartości rzeczywistych i przewidywanych'):
    """
    Tworzy wykres porównujący wartości rzeczywiste z przewidywanymi dla modelu regresji.
    
    Parameters:
    -----------
    y_true : array-like
        Rzeczywiste wartości
    y_pred : array-like
        Przewidywane wartości
    title : str, default='Porównanie wartości rzeczywistych i przewidywanych'
        Tytuł wykresu
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    
    # Dodanie linii idealnej predykcji (y=x)
    min_val = min(min(y_true), min(y_pred))
    max_val = max(max(y_true), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.title(title)
    plt.xlabel('Wartości rzeczywiste')
    plt.ylabel('Wartości przewidywane')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'regression_results.png'))
    plt.close()
    
def plot_feature_importance(feature_names, importances, title='Ważność cech'):
    """
    Tworzy wykres słupkowy przedstawiający ważność cech.
    
    Parameters:
    -----------
    feature_names : array-like
        Nazwy cech
    importances : array-like
        Ważność cech
    title : str, default='Ważność cech'
        Tytuł wykresu
    """
    # Sortowanie cech wg ważności
    indices = np.argsort(importances)
    sorted_names = [feature_names[i] for i in indices]
    sorted_importances = importances[indices]
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(sorted_names)), sorted_importances, align='center')
    plt.yticks(range(len(sorted_names)), sorted_names)
    plt.xlabel('Ważność')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'feature_importance.png'))
    plt.close()
    
def plot_confusion_matrix(y_true, y_pred, class_names=None, title='Macierz pomyłek'):
    """
    Tworzy wizualizację macierzy pomyłek.
    
    Parameters:
    -----------
    y_true : array-like
        Rzeczywiste etykiety
    y_pred : array-like
        Przewidywane etykiety
    class_names : list, default=None
        Nazwy klas
    title : str, default='Macierz pomyłek'
        Tytuł wykresu
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names if class_names else 'auto',
                yticklabels=class_names if class_names else 'auto')
    plt.title(title)
    plt.ylabel('Etykieta rzeczywista')
    plt.xlabel('Etykieta przewidywana')
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'confusion_matrix.png'))
    plt.close()
    
def plot_learning_curves(train_scores, test_scores, train_sizes, metric_name='Score'):
    """
    Tworzy wykres krzywych uczenia.
    
    Parameters:
    -----------
    train_scores : array-like
        Wyniki na zbiorze treningowym
    test_scores : array-like
        Wyniki na zbiorze testowym
    train_sizes : array-like
        Rozmiary zbiorów treningowych
    metric_name : str, default='Score'
        Nazwa metryki
    """
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label=f'Zbiór treningowy')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(train_sizes, test_mean, 'o-', color='orange', label=f'Zbiór testowy')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='orange')
    
    plt.title('Krzywe uczenia')
    plt.xlabel('Liczba próbek treningowych')
    plt.ylabel(metric_name)
    plt.grid(True)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'learning_curves.png'))
    plt.close() 