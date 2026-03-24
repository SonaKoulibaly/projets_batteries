# API Flask - SoH Predictor

API REST pour prédire l'état de santé des batteries avec un modèle LSTM.

## 🚀 Déploiement sur Hugging Face Spaces

### Étapes :

1. **Créer un Space sur Hugging Face**
   - Aller sur https://huggingface.co/spaces
   - Cliquer sur "Create new Space"
   - Choisir "Gradio" comme SDK
   - Nom : `battery-soh-api`

2. **Cloner le repo**
```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/battery-soh-api
   cd battery-soh-api
```

3. **Copier les fichiers**
   - Copier `app.py` et `requirements.txt`
   - Copier le dossier `models/` et `data/processed/`

4. **Pousser sur HF**
```bash
   git add .
   git commit -m "Initial commit"
   git push
```

5. **URL publique**
```
   http://127.0.0.1:7860
```

## 📡 Endpoints

### GET `/`
Informations sur l'API

### GET `/health`
Statut de santé

### GET `/model-info`
Informations sur le modèle

### POST `/predict`
Faire une prédiction

**Body :**
```json
{
  "data": [
    {
      "Voltage_measured": 3.5,
      "Current_measured": 1.2,
      "Temperature_measured": 25,
      "SoC": 0.5,
      "cycle_number": 1
    }
  ]
}
```

**Response :**
```json
{
  "success": true,
  "predictions": [82.5, 82.3, ...],
  "statistics": {
    "mean": 82.4,
    "min": 82.1,
    "max": 82.7
  }
}
```

## 🧪 Test Local
```bash
pip install -r requirements.txt
python app.py
```

Ouvrir http://localhost:7860