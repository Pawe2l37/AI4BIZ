import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc
from sklearn.model_selection import learning_curve
import os

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
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names if class_names else 'auto',
                yticklabels=class_names if class_names else 'auto')
    plt.title(title, fontsize=16)
    plt.ylabel('Etykieta rzeczywista', fontsize=14)
    plt.xlabel('Etykieta przewidywana', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'confusion_matrix.png'), dpi=300)
    plt.close()

def plot_feature_importance(feature_names, importances, title='Ważność cech', top_n=10):
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
    top_n : int, default=10
        Liczba najważniejszych cech do wyświetlenia
    """
    # Sortowanie cech wg ważności (malejąco)
    indices = np.argsort(importances)[::-1]
    top_indices = indices[:top_n]
    
    sorted_names = [feature_names[i] for i in top_indices]
    sorted_importances = importances[top_indices]
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(sorted_names)))
    
    plt.barh(range(len(sorted_names)), sorted_importances, align='center', color=colors)
    plt.yticks(range(len(sorted_names)), sorted_names, fontsize=12)
    plt.xlabel('Ważność', fontsize=14)
    plt.title(title, fontsize=16)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'feature_importance.png'), dpi=300)
    plt.close()

def plot_learning_curves(estimator, X, y, title='Krzywe uczenia', cv=5, n_jobs=None, train_sizes=np.linspace(0.1, 1.0, 5)):
    """
    Tworzy wykres krzywych uczenia dla modelu.
    
    Parameters:
    -----------
    estimator : estimator object
        Model uczenia maszynowego
    X : array-like
        Dane wejściowe
    y : array-like
        Etykiety
    title : str, default='Krzywe uczenia'
        Tytuł wykresu
    cv : int, cross-validation generator
        Określa strategię walidacji krzyżowej
    n_jobs : int, default=None
        Liczba rdzeni używanych do obliczeń
    train_sizes : array-like, default=np.linspace(0.1, 1.0, 5)
        Rozmiary zbiorów treningowych
    """
    plt.figure(figsize=(12, 8))
    
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes,
        scoring='accuracy'
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    plt.plot(train_sizes, train_mean, 'o-', color='#4C72B0', label=f'Zbiór treningowy')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='#4C72B0')
    
    plt.plot(train_sizes, test_mean, 'o-', color='#C44E52', label=f'Zbiór testowy (walidacja krzyżowa)')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='#C44E52')
    
    plt.title(title, fontsize=16)
    plt.xlabel('Liczba próbek treningowych', fontsize=14)
    plt.ylabel('Dokładność', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='lower right', fontsize=12)
    plt.ylim([0.5, 1.05])
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'learning_curves.png'), dpi=300)
    plt.close()

def plot_roc_curve(y_true, y_score, title='Krzywa ROC'):
    """
    Tworzy wykres krzywej ROC.
    
    Parameters:
    -----------
    y_true : array-like
        Rzeczywiste etykiety
    y_score : array-like
        Przewidywane prawdopodobieństwa
    title : str, default='Krzywa ROC'
        Tytuł wykresu
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='lower right', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'roc_curve.png'), dpi=300)
    plt.close()

def plot_precision_recall_curve(y_true, y_score, title='Krzywa Precision-Recall'):
    """
    Tworzy wykres krzywej Precision-Recall.
    
    Parameters:
    -----------
    y_true : array-like
        Rzeczywiste etykiety
    y_score : array-like
        Przewidywane prawdopodobieństwa
    title : str, default='Krzywa Precision-Recall'
        Tytuł wykresu
    """
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    pr_auc = auc(recall, precision)
    
    plt.figure(figsize=(10, 8))
    plt.plot(recall, precision, lw=2, label=f'PR curve (AUC = {pr_auc:.3f})')
    plt.xlabel('Recall', fontsize=14)
    plt.ylabel('Precision', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='lower left', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'precision_recall_curve.png'), dpi=300)
    plt.close()

def plot_decision_regions(X, y, classifier, title='Regiony decyzyjne', feature_indices=None):
    """
    Tworzy wizualizację regionów decyzyjnych dla dwóch wybranych cech.
    
    Parameters:
    -----------
    X : array-like
        Dane wejściowe
    y : array-like
        Etykiety
    classifier : estimator object
        Wytrenowany klasyfikator
    title : str, default='Regiony decyzyjne'
        Tytuł wykresu
    feature_indices : list, default=None
        Indeksy dwóch cech do wizualizacji (jeśli None, wybierane są dwie pierwsze cechy)
    """
    if feature_indices is None:
        feature_indices = [0, 1]
    
    if len(feature_indices) != 2:
        raise ValueError("Należy wybrać dokładnie dwie cechy do wizualizacji")
    
    # Wybieramy dwie cechy
    X_selected = X[:, feature_indices]
    
    # Tworzymy siatkę punktów do predykcji
    x_min, x_max = X_selected[:, 0].min() - 1, X_selected[:, 0].max() + 1
    y_min, y_max = X_selected[:, 1].min() - 1, X_selected[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))
    
    # Przygotowujemy dane testowe dla naszej siatki
    Z_input = np.c_[xx.ravel(), yy.ravel()]
    # Uzupełniamy brakujące cechy zerami, jeśli X ma więcej niż 2 wymiary
    if X.shape[1] > 2:
        Z_full = np.zeros((Z_input.shape[0], X.shape[1]))
        Z_full[:, feature_indices] = Z_input
        Z = classifier.predict(Z_full)
    else:
        Z = classifier.predict(Z_input)
    
    # Przekształcamy wynik z powrotem do kształtu siatki
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(12, 10))
    # Rysujemy regiony decyzyjne
    plt.contourf(xx, yy, Z, alpha=0.4, cmap='viridis')
    
    # Rysujemy punkty danych
    scatter = plt.scatter(X_selected[:, 0], X_selected[:, 1], c=y, 
                         edgecolor='k', s=100, cmap='viridis', alpha=0.8)
    
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    
    # Dodajemy etykiety osi i tytuł
    feature_names = [f"Cecha {i}" for i in feature_indices]
    plt.xlabel(feature_names[0], fontsize=14)
    plt.ylabel(feature_names[1], fontsize=14)
    plt.title(title, fontsize=16)
    plt.colorbar(scatter, label='Klasa')
    plt.tight_layout()
    plt.savefig(os.path.join('wykresy', 'decision_regions.png'), dpi=300)
    plt.close() 