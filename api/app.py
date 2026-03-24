"""
API Flask pour la prédiction SoH des batteries
Déployable sur Hugging Face Spaces
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
CORS(app)  # Permettre les requêtes du frontend

# Chemins (en dur pour éviter problème accent)
import os
BASE_DIR = r'C:\Users\HP\Desktop\Mastère-2-Big-Data-Data-Strategy\Deeplearning MLOPS\projets_batteries'
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'lstm_soh_final.h5')  # Utilise lstm_soh_final.h5
SCALER_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'scaler.pkl')
METADATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'metadata.pkl')

# Charger le modèle au démarrage
print("🔧 Chargement du modèle...")
try:
    model = keras.models.load_model(str(MODEL_PATH))
    print("✅ Modèle chargé")
except Exception as e:
    print(f"❌ Erreur chargement modèle : {e}")
    model = None

try:
    with open(str(SCALER_PATH), 'rb') as f:
        scaler = pickle.load(f)
    print("✅ Scaler chargé")
except Exception as e:
    print(f"❌ Erreur chargement scaler : {e}")
    scaler = None

try:
    with open(str(METADATA_PATH), 'rb') as f:
        metadata = pickle.load(f)
    print("✅ Metadata chargées")
except Exception as e:
    print(f"❌ Erreur chargement metadata : {e}")
    metadata = {'window_size': 20, 'feature_columns': []}


@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'name': 'SoH Predictor API',
        'version': '1.0.0',
        'status': 'running',
        'model_loaded': model is not None,
        'endpoints': {
            '/': 'API info',
            '/health': 'Health check',
            '/predict': 'POST - Faire une prédiction',
            '/model-info': 'Informations sur le modèle'
        }
    })


@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({
        'status': 'healthy',
        'model': 'loaded' if model else 'not loaded',
        'scaler': 'loaded' if scaler else 'not loaded'
    })


@app.route('/model-info')
def model_info():
    """Informations sur le modèle"""
    return jsonify({
        'architecture': 'LSTM',
        'window_size': metadata.get('window_size', 20),
        'n_features': metadata.get('n_features', 15),
        'features': metadata.get('feature_columns', []),
        'performance': {
            'R2': 0.845,
            'MAE': 2.15,
            'RMSE': 2.66
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction
    
    Body JSON:
    {
        "data": [
            {
                "Voltage_measured": 3.5,
                "Current_measured": 1.2,
                "Temperature_measured": 25,
                "SoC": 0.5,
                "cycle_number": 1
            },
            ... (minimum 20 mesures)
        ]
    }
    """
    if not model or not scaler:
        return jsonify({'error': 'Modèle non chargé'}), 500
    
    try:
        # Récupérer les données
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({'error': 'Format invalide. Attendu: {"data": [...]}'}), 400
        
        # Convertir en DataFrame
        df = pd.DataFrame(data['data'])
        
        # Vérifier le nombre de mesures
        window_size = metadata.get('window_size', 20)
        if len(df) < window_size:
            return jsonify({
                'error': f'Minimum {window_size} mesures requises. Reçu: {len(df)}'
            }), 400
        
        # Vérifier les colonnes
        required_cols = ['Voltage_measured', 'Current_measured', 
                        'Temperature_measured', 'SoC', 'cycle_number']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            return jsonify({'error': f'Colonnes manquantes: {missing_cols}'}), 400
        
        # Normaliser
        data_scaled = scaler.transform(df[required_cols])
        
        # Créer séquences
        sequences = []
        for i in range(len(data_scaled) - window_size + 1):
            sequences.append(data_scaled[i:i + window_size])
        
        X = np.array(sequences)
        
        # Prédire
        predictions = model.predict(X, verbose=0).flatten()
        
        # Retourner résultats
        return jsonify({
            'success': True,
            'predictions': predictions.tolist(),
            'statistics': {
                'mean': float(predictions.mean()),
                'min': float(predictions.min()),
                'max': float(predictions.max()),
                'std': float(predictions.std())
            },
            'n_predictions': len(predictions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))  # Port Hugging Face
    app.run(host='0.0.0.0', port=port, debug=False)