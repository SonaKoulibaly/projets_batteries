# 🔋 SoH Predictor - Battery Health Prediction System

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)](https://huggingface.co/spaces/ONA6/battery-soh-api)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black)](https://battery-soh-predictor.vercel.app)

Système intelligent de prédiction de l'état de santé (SoH) des batteries lithium-ion utilisant des réseaux LSTM.

---

## 🎯 Démonstration

### 🌐 Applications Déployées

- **🎨 Frontend (Dashboard)** : [https://battery-soh-predictor.vercel.app](https://battery-soh-predictor.vercel.app)
- **🔌 API Backend** : [https://ona6-battery-soh-api.hf.space](https://ona6-battery-soh-api.hf.space)

### 📊 Performances du Modèle

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **R² Score** | 84.5% | ✅ Excellent |
| **MAE** | 2.15% | ✅ Très bon |
| **RMSE** | 2.66% | ✅ Très bon |
| **Précision ±5%** | 96.7% | ✅ Outstanding |

---

## 🚀 Aperçu du Projet

### Objectif

Prédire l'état de santé (State of Health - SoH) des batteries lithium-ion à partir de mesures électriques et thermiques issues de cycles de charge/décharge.

### Applications

- 🚗 **Véhicules électriques** : Estimation de l'autonomie
- ⚡ **Stockage d'énergie** : Maintenance prédictive
- 📱 **IoT & Systèmes embarqués** : Monitoring temps réel
- 🏭 **Industrie** : Optimisation de la durée de vie

---

## 🏗️ Architecture

### Stack Technologique

**Backend & Modèle**
- Python 3.10
- TensorFlow 2.15 / Keras
- Flask REST API
- NumPy, Pandas, Scikit-learn

**Frontend**
- HTML5, CSS3, JavaScript
- Tailwind CSS
- Chart.js
- Vercel (Hosting)

**Déploiement**
- Hugging Face Spaces (API)
- Vercel (Frontend)
- Docker

### Architecture LSTM
```
Input (20 timesteps, 15 features)
    ↓
LSTM (256 neurones) + Dropout (30%)
    ↓
LSTM (128 neurones) + Dropout (30%)
    ↓
Dense (32 neurones) + Dropout (30%)
    ↓
Dense (1 neurone) → SoH
```

**Total** : 889,409 paramètres entraînables

---

## 📊 Dataset

- **Source** : Mesures réelles de batteries lithium-ion
- **Taille** : ~29,000 mesures
- **Batteries** : 24 unités
- **Features** : 15 (5 brutes + 10 engineerées)
- **Split** : 80% train / 10% val / 10% test (temporel)

### Features Utilisées

**Brutes (5)** :
- Voltage_measured, Current_measured, Temperature_measured, SoC, cycle_number

**Engineerées (10)** :
- Dérivées temporelles (3)
- Moyennes mobiles (3)
- Interactions (3)
- Normalisation (1)

---

## 🛠️ Installation

### Prérequis

- Python 3.10+
- pip

### Installation Locale
```bash
# Cloner le repo
git clone https://github.com/YOUR_USERNAME/projets_batteries.git
cd projets_batteries

# Créer environnement virtuel
python -m venv .venv

# Activer environnement
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
```

---

## 💻 Utilisation

### Option 1 : Notebooks Jupyter
```bash
jupyter notebook
```

Exécuter dans l'ordre :
1. `01_exploration_donnees.ipynb`
2. `02_preprocessing.ipynb`
3. `03_modelisation_lstm.ipynb`
4. `04_evaluation_resultats.ipynb`

### Option 2 : Script Python
```python
from src.predict import BatteryHealthPredictor
import pandas as pd

# Initialiser prédicteur
predictor = BatteryHealthPredictor()

# Charger données (minimum 20 mesures)
data = pd.read_csv('mes_donnees.csv')

# Prédire
predictions = predictor.predict(data)
print(f"SoH prédit : {predictions[-1]:.2f}%")
```

### Option 3 : API REST
```bash
# Démarrer l'API localement
cd api
python app.py
```

Tester avec curl :
```bash
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [...]}'
```

---

## 🚀 Déploiement

### API (Hugging Face Spaces)

Voir [`DEPLOYMENT.md`](DEPLOYMENT.md) pour les instructions détaillées.

URL : [https://ona6-battery-soh-api.hf.space](https://ona6-battery-soh-api.hf.space)

### Frontend (Vercel)

1. Fork ce repo
2. Connecter à Vercel
3. Root Directory : `frontend`
4. Deploy

URL : [https://battery-soh-predictor.vercel.app](https://battery-soh-predictor.vercel.app)

---

## 📁 Structure du Projet
```
projets_batteries/
├── api/                     # API Flask
├── frontend/                # Dashboard web
├── notebooks/               # Notebooks Jupyter
├── src/                     # Code source Python
├── models/                  # Modèles entraînés (.h5)
├── data/                    # Données (raw + processed)
├── results/                 # Résultats & graphiques
├── docs/                    # Documentation
├── config/                  # Configuration
├── tests/                   # Tests unitaires
└── README.md                # Ce fichier
```

---

## 📚 Documentation

- **Architecture** : [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- **Questions de réflexion** : [`docs/QUESTIONS_REFLEXION.md`](docs/QUESTIONS_REFLEXION.md)
- **Guide de déploiement** : [`DEPLOYMENT.md`](DEPLOYMENT.md)

---

## 🧪 Tests
```bash
# Lancer les tests unitaires
python -m pytest tests/

# Test spécifique
python tests/test_preprocessing.py
```

---

## 📈 Résultats

### Métriques Finales
```
MAE  : 2.15%  ✅
RMSE : 2.66%  ✅
R²   : 0.845  ✅
MAPE : 2.80%  ✅
```

### Visualisations

Voir `results/figures/` pour :
- Courbes d'entraînement
- Prédictions vs valeurs réelles
- Distribution des erreurs
- Analyse par batterie

---

## 🤝 Contribution

Ce projet a été réalisé dans le cadre du **Mastère 2 Big Data** - Deep Learning.

### Auteur

**Sona KOULIBALY**

- 🎓 Mastère 2 Big Data
- 📅 Mars 2026

---

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- Dataset : NASA Battery Dataset
- Frameworks : TensorFlow, Flask, Vercel, Hugging Face
- Inspiration : Littérature scientifique sur Battery Health Prediction

---

## 📞 Contact

Pour toute question sur le projet :
- 🌐 Portfolio : https://github.com/SonaKoulibaly
- 💼 LinkedIn : https://www.linkedin.com/in/sona-koulibaly/
- 📧 Email : sonakoul.pro@gmail.com

---

<div align="center">

**⚡ Fait avec passion pour l'IA et les batteries du futur ⚡**

</div>