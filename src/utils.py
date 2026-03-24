"""
Fonctions utilitaires pour le projet
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def calculate_metrics(y_true, y_pred):
    """
    Calculer toutes les métriques de performance
    
    Args:
        y_true: Vraies valeurs
        y_pred: Prédictions
        
    Returns:
        dict avec les métriques
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # MAPE
    mape = np.mean(np.abs((y_true - y_pred) / np.clip(y_true, 1e-10, None))) * 100
    
    # Erreur max
    max_error = np.max(np.abs(y_true - y_pred))
    
    # Pourcentages dans marges
    within_5pct = np.sum(np.abs(y_true - y_pred) <= 5) / len(y_true) * 100
    within_10pct = np.sum(np.abs(y_true - y_pred) <= 10) / len(y_true) * 100
    
    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'mape': mape,
        'max_error': max_error,
        'within_5pct': within_5pct,
        'within_10pct': within_10pct
    }


def plot_predictions(y_true, y_pred, title="Prédictions vs Vraies Valeurs", save_path=None):
    """
    Créer un graphique prédictions vs vraies valeurs
    
    Args:
        y_true: Vraies valeurs
        y_pred: Prédictions
        title: Titre du graphique
        save_path: Chemin pour sauvegarder (optionnel)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot
    ax.scatter(y_true, y_pred, alpha=0.6, s=40, color='steelblue', 
               edgecolor='black', linewidth=0.5)
    
    # Ligne parfaite
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 
            'r--', linewidth=2.5, label='Prédiction parfaite')
    
    # Zone ±5%
    ax.fill_between([min_val, max_val], 
                     [min_val-5, max_val-5], 
                     [min_val+5, max_val+5],
                     alpha=0.2, color='green', label='Marge ±5%')
    
    ax.set_xlabel('Vraies valeurs (SoH %)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Prédictions (SoH %)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_error_distribution(y_true, y_pred, save_path=None):
    """
    Afficher la distribution des erreurs
    
    Args:
        y_true: Vraies valeurs
        y_pred: Prédictions
        save_path: Chemin pour sauvegarder (optionnel)
    """
    errors = y_true - y_pred
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(errors, bins=50, color='teal', edgecolor='black', alpha=0.7)
    ax.axvline(0, color='red', linestyle='--', linewidth=2.5, label='Erreur = 0')
    ax.axvline(errors.mean(), color='orange', linestyle='--', linewidth=2,
               label=f'Moyenne = {errors.mean():.2f}%')
    
    ax.set_xlabel('Erreur (Vrai - Prédit) %', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fréquence', fontsize=12, fontweight='bold')
    ax.set_title('Distribution des Erreurs', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def create_sliding_windows(df, window_size, feature_cols, target_col='SoH', group_col='battery_id'):
    """
    Créer des fenêtres glissantes pour LSTM
    
    Args:
        df: DataFrame
        window_size: Taille de la fenêtre
        feature_cols: Colonnes de features
        target_col: Colonne cible
        group_col: Colonne de groupement
        
    Returns:
        X, y, ids
    """
    X = []
    y = []
    ids = []
    
    for group_id in df[group_col].unique():
        group_data = df[df[group_col] == group_id].copy()
        group_data = group_data.sort_values('cycle_number').reset_index(drop=True)
        
        for i in range(len(group_data) - window_size + 1):
            window = group_data.iloc[i:i+window_size]
            X.append(window[feature_cols].values)
            y.append(window[target_col].iloc[-1])
            ids.append(group_id)
    
    return np.array(X), np.array(y), np.array(ids)


def print_metrics_summary(metrics):
    """
    Afficher un résumé des métriques
    
    Args:
        metrics: dict de métriques
    """
    print("=" * 70)
    print("📊 RÉSUMÉ DES MÉTRIQUES")
    print("=" * 70)
    print(f"\n   MAE  : {metrics['mae']:.4f}%")
    print(f"   RMSE : {metrics['rmse']:.4f}%")
    print(f"   R²   : {metrics['r2']:.4f} ({metrics['r2']*100:.2f}%)")
    print(f"   MAPE : {metrics['mape']:.2f}%")
    print(f"\n   Erreur max : {metrics['max_error']:.2f}%")
    print(f"   Dans ±5%   : {metrics['within_5pct']:.1f}%")
    print(f"   Dans ±10%  : {metrics['within_10pct']:.1f}%")
    print("=" * 70)