# Architecture du Projet - Prédiction SoH Batteries

## 📋 Vue d'ensemble

Ce projet implémente un modèle LSTM (Long Short-Term Memory) pour prédire l'état de santé (SoH - State of Health) des batteries lithium-ion à partir de mesures de cycles de charge/décharge.

---

## 🏗️ Structure du Projet
```
PROJETS_BATTERIES/
│
├── data/
│   ├── raw/                          # Données brutes
│   │   └── battery_health_dataset.csv
│   └── processed/                    # Données préparées
│       ├── X_train.npy
│       ├── X_val.npy
│       ├── X_test.npy
│       ├── y_train.npy
│       ├── y_val.npy
│       ├── y_test.npy
│       ├── scaler.pkl
│       └── metadata.pkl
│
├── notebooks/                        # Notebooks Jupyter
│   ├── 00_DEBUG_DIAGNOSTIC.ipynb    # Debug et diagnostics
│   ├── 01_exploration_donnees.ipynb # EDA
│   ├── 02_preprocessing.ipynb       # Préparation données
│   ├── 03_modelisation_lstm.ipynb   # Entraînement LSTM
│   └── 04_evaluation_resultats.ipynb# Évaluation
│
├── src/                              # Code source Python
│   ├── predict.py                   # Script de prédiction
│   └── utils.py                     # Fonctions utilitaires
│
├── models/                           # Modèles entraînés
│   ├── lstm_soh_best.h5            # Meilleur modèle
│   ├── lstm_soh_final.h5           # Modèle final
│   └── training_history.json       # Historique entraînement
│
├── results/                          # Résultats
│   ├── metrics/                     # Métriques
│   │   ├── evaluation_metrics.json
│   │   ├── predictions_detailed.csv
│   │   └── battery_statistics.csv
│   └── figures/                     # Graphiques
│       ├── predictions_vs_actual.png
│       ├── error_by_battery.png
│       └── error_analysis.png
│
├── docs/                             # Documentation
│   ├── ARCHITECTURE.md              # Ce fichier
│   └── GUIDE_UTILISATION.md         # Guide utilisateur
│
├── config/                           # Configuration
│   └── config.yaml                  # Paramètres du projet
│
├── requirements.txt                  # Dépendances Python
├── .gitignore                       # Fichiers à ignorer
└── README.md                        # Documentation principale
```

---

## 🔄 Pipeline de Traitement

### 1. **Exploration des Données** (`01_exploration_donnees.ipynb`)
- Chargement du dataset
- Analyse statistique descriptive
- Visualisation des distributions
- Détection de valeurs aberrantes
- Analyse des corrélations

### 2. **Preprocessing** (`02_preprocessing.ipynb`)
- **Nettoyage** : Suppression des valeurs SoH > 100%
- **Feature Engineering** :
  - Dérivées temporelles (changements)
  - Moyennes mobiles (tendances)
  - Interactions entre features
  - Normalisation des cycles
- **Normalisation** : MinMaxScaler sur les features (SoH non normalisé)
- **Fenêtres glissantes** : Séquences de 20 mesures consécutives
- **Split temporel** : 80% train, 10% val, 10% test

### 3. **Modélisation LSTM** (`03_modelisation_lstm.ipynb`)
- **Architecture** :
  - LSTM (256 neurones) + Dropout (30%)
  - LSTM (128 neurones) + Dropout (30%)
  - Dense (32 neurones) + Dropout (30%)
  - Dense (1 neurone, sortie)
- **Compilation** :
  - Optimizer : Adam (LR = 0.001)
  - Loss : MSE
  - Metrics : MAE
- **Callbacks** :
  - EarlyStopping (patience=20)
  - ModelCheckpoint
  - ReduceLROnPlateau
- **Entraînement** : Batch size=64, Epochs max=200

### 4. **Évaluation** (`04_evaluation_resultats.ipynb`)
- Calcul des métriques (MAE, RMSE, R², MAPE)
- Visualisations (scatter plots, distributions)
- Analyse par batterie
- Sauvegarde des résultats

---

## 📊 Données

### Dataset
- **Source** : `battery_health_dataset.csv`
- **Taille** : ~29,000 mesures
- **Batteries** : 24 unités
- **Features brutes** :
  - `Voltage_measured` : Tension (V)
  - `Current_measured` : Courant (A)
  - `Temperature_measured` : Température (°C)
  - `SoC` : State of Charge (%)
  - `cycle_number` : Numéro du cycle
  - `battery_id` : Identifiant batterie
- **Cible** : `SoH` (State of Health, %)

### Features Engineerées
- **Dérivées** : `Voltage_diff`, `SoC_diff`, `Temp_diff`
- **Moyennes mobiles** : `Voltage_ma3`, `SoC_ma3`, `Temp_ma3`
- **Interactions** : `Voltage_x_SoC`, `Current_x_Temp`, `Voltage_per_SoC`
- **Normalisations** : `cycle_normalized`

**Total** : 15 features

---

## 🧠 Modèle LSTM

### Architecture Détaillée
```
Input: (batch_size, 20, 15)
   ↓
LSTM(256) + Dropout(0.3)
   ↓
LSTM(128) + Dropout(0.3)
   ↓
Dense(32, relu) + Dropout(0.3)
   ↓
Dense(1)
   ↓
Output: (batch_size, 1)
```

**Paramètres** : 889,409 poids entraînables

### Hyperparamètres Optimaux
- Window size : 20
- LSTM units : 256, 128
- Dropout : 30%
- Learning rate : 0.001
- Batch size : 64

---

## 📈 Performances

### Résultats Finaux
```
MAE  : 2.15%
RMSE : 2.66%
R²   : 0.845 (84.5%)
MAPE : 2.80%
```

### Interprétation
- ✅ **96.7%** des prédictions dans ±5%
- ✅ **100%** des prédictions dans ±10%
- ✅ Performance **excellente** pour ce type de problème

---

## 🔧 Technologies Utilisées

- **Python** : 3.10.11
- **TensorFlow/Keras** : 2.15.0
- **NumPy** : 1.24.3
- **Pandas** : 2.0.3
- **Scikit-learn** : 1.3.0
- **Matplotlib/Seaborn** : Visualisation

---

## 🚀 Utilisation

### Prédiction sur Nouvelles Données
```python
from src.predict import BatteryHealthPredictor

# Initialiser
predictor = BatteryHealthPredictor()

# Prédire
predictions = predictor.predict(new_data)
```

Voir `docs/GUIDE_UTILISATION.md` pour plus de détails.

---

## 📝 Améliorations Futures

1. **Données** : Collecter plus de batteries (objectif : 50+)
2. **Features** : Ajouter dérivées secondes, entropie
3. **Architecture** : Tester Bidirectional LSTM, Transformers
4. **Hyperparamètres** : GridSearch automatisé
5. **Déploiement** : API REST, Dashboard Streamlit

---

## 👨‍💻 Auteur Sona KOULIBALY

**Projet réalisé dans le cadre du Mastère 2 Big Data - Deep Learning & MLOPS**

Date : Mars 2026