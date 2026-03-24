# 🚀 Guide de Déploiement Complet

Ce guide explique comment déployer l'API et le Dashboard en production.

---

## 📋 Architecture Finale
```
┌─────────────────────────────────────┐
│  Frontend (Vercel)                  │
│  https://battery-soh.vercel.app     │
└──────────────┬──────────────────────┘
               │ API Calls
               ↓
┌─────────────────────────────────────┐
│  Backend API (Hugging Face Spaces)  │
│  https://USER-battery-api.hf.space  │
└─────────────────────────────────────┘
```

---

## 🔧 PARTIE 1 : Déployer l'API sur Hugging Face Spaces

### Étape 1 : Créer un Space

1. Aller sur **https://huggingface.co/spaces**
2. Cliquer sur **"Create new Space"**
3. Configuration :
   - **Name** : `battery-soh-api`
   - **License** : MIT
   - **SDK** : Gradio
   - **Hardware** : CPU basic (gratuit)
4. Cliquer sur **"Create Space"**

### Étape 2 : Préparer les Fichiers

Dans un nouveau dossier temporaire :
```bash
mkdir hf-deployment
cd hf-deployment
```

Copier ces fichiers :
- `api/app.py`
- `api/requirements.txt`
- `models/lstm_soh_best.h5`
- `data/processed/scaler.pkl`
- `data/processed/metadata.pkl`

Structure finale :
```
hf-deployment/
├── app.py
├── requirements.txt
├── models/
│   └── lstm_soh_best.h5
└── data/
    └── processed/
        ├── scaler.pkl
        └── metadata.pkl
```

### Étape 3 : Modifier `app.py`

Dans `app.py`, **modifier les chemins** :
```python
# AVANT (chemins locaux)
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'lstm_soh_best.h5'

# APRÈS (chemins HuggingFace)
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / 'models' / 'lstm_soh_best.h5'
```

### Étape 4 : Pousser sur Hugging Face
```bash
# Cloner votre Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/battery-soh-api
cd battery-soh-api

# Copier tous les fichiers
cp -r ../hf-deployment/* .

# Git LFS pour les gros fichiers
git lfs install
git lfs track "*.h5"
git lfs track "*.pkl"

# Commit et push
git add .
git commit -m "Initial deployment"
git push
```

### Étape 5 : Vérifier le Déploiement

- Le Space va builder automatiquement (~5 min)
- URL finale : `https://YOUR_USERNAME-battery-soh-api.hf.space`
- Tester : Ouvrir l'URL dans le navigateur
- Vous devriez voir le JSON de l'API

---

## 🎨 PARTIE 2 : Déployer le Frontend sur Vercel

### Étape 1 : Pousser sur GitHub
```bash
# Depuis la racine du projet
git add frontend/
git commit -m "Add frontend dashboard"
git push origin main
```

### Étape 2 : Importer sur Vercel

1. Aller sur **https://vercel.com**
2. Cliquer sur **"New Project"**
3. **Import Git Repository** → Sélectionner votre repo
4. Configuration :
   - **Project Name** : `battery-soh-predictor`
   - **Framework Preset** : Other
   - **Root Directory** : `frontend`
   - **Build Command** : (laisser vide)
   - **Output Directory** : (laisser vide)
5. Cliquer sur **"Deploy"**

### Étape 3 : Connecter l'API

Une fois déployé :

1. Récupérer l'URL de votre API Hugging Face :
```
   https://YOUR_USERNAME-battery-soh-api.hf.space
```

2. Modifier `frontend/app.js` ligne 2 :
```javascript
   const API_URL = 'https://YOUR_USERNAME-battery-soh-api.hf.space';
```

3. Re-commit et push :
```bash
   git add frontend/app.js
   git commit -m "Update API URL"
   git push
```

4. Vercel va automatiquement re-déployer

### Étape 4 : Ajouter le Logo

1. Copier `logo.png` dans `frontend/`
2. Commit et push :
```bash
   git add frontend/logo.png
   git commit -m "Add logo"
   git push
```

---

## ✅ PARTIE 3 : Vérification Finale

### Test Complet

1. **Ouvrir le Frontend** : `https://battery-soh-predictor.vercel.app`
2. **Uploader un CSV de test** (au moins 20 lignes)
3. **Cliquer sur "PRÉDIRE LE SoH"**
4. **Vérifier les résultats** : Graphique + Stats

### Résolution de Problèmes

**Problème : "Error: Failed to fetch"**
- Solution : Vérifier que l'URL API dans `app.js` est correcte
- Tester l'API directement dans le navigateur

**Problème : "CORS error"**
- Solution : Vérifier que `flask-cors` est bien installé dans l'API

**Problème : "Model not loaded"**
- Solution : Vérifier que les fichiers `.h5` et `.pkl` sont bien sur HuggingFace
- Vérifier Git LFS

---

## 🎯 URLs Finales

Une fois déployé, vous aurez :

- **Frontend** : `https://battery-soh-predictor.vercel.app`
- **API** : `https://YOUR_USERNAME-battery-soh-api.hf.space`

Ajoutez ces liens sur :
- ✅ README.md
- ✅ CV
- ✅ LinkedIn
- ✅ Portfolio

---

## 📱 Liens Utiles

- **Hugging Face Docs** : https://huggingface.co/docs/hub/spaces
- **Vercel Docs** : https://vercel.com/docs
- **Git LFS** : https://git-lfs.github.com

---

## 🔐 Sécurité

- ✅ Pas de clés API dans le code
- ✅ CORS configuré
- ✅ HTTPS automatique (Vercel + HF)

---

**Bon déploiement ! 🚀**