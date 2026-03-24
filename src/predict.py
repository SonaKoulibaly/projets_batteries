"""
Script de prédiction SoH - Batteries
Utilise le modèle LSTM entraîné pour prédire l'état de santé des batteries
"""

import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
from tensorflow import keras

class BatteryHealthPredictor:
    """
    Classe pour prédire le SoH des batteries
    """
    
    def __init__(self, model_path='../models/lstm_soh_best.h5', 
                 scaler_path='../data/processed/scaler.pkl',
                 metadata_path='../data/processed/metadata.pkl'):
        """
        Initialiser le prédicteur
        
        Args:
            model_path: Chemin vers le modèle entraîné
            scaler_path: Chemin vers le scaler
            metadata_path: Chemin vers les métadonnées
        """
        self.model_path = Path(model_path)
        self.scaler_path = Path(scaler_path)
        self.metadata_path = Path(metadata_path)
        
        # Charger le modèle
        print(f"🔧 Chargement du modèle depuis {self.model_path}")
        self.model = keras.models.load_model(str(self.model_path))
        
        # Charger le scaler
        print(f"🔧 Chargement du scaler depuis {self.scaler_path}")
        with open(str(self.scaler_path), 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Charger les métadonnées
        print(f"🔧 Chargement des métadonnées depuis {self.metadata_path}")
        with open(str(self.metadata_path), 'rb') as f:
            self.metadata = pickle.load(f)
        
        self.window_size = self.metadata['window_size']
        self.feature_columns = self.metadata['feature_columns']
        
        print(f"✅ Prédicteur initialisé")
        print(f"   Window size : {self.window_size}")
        print(f"   Features : {len(self.feature_columns)}")
    
    def preprocess_data(self, data):
        """
        Prétraiter les données brutes
        
        Args:
            data: DataFrame avec les features brutes
            
        Returns:
            Données normalisées
        """
        # Vérifier que toutes les colonnes sont présentes
        missing_cols = set(self.feature_columns) - set(data.columns)
        if missing_cols:
            raise ValueError(f"Colonnes manquantes : {missing_cols}")
        
        # Sélectionner et normaliser
        data_scaled = self.scaler.transform(data[self.feature_columns])
        
        return data_scaled
    
    def create_sequences(self, data_scaled):
        """
        Créer des séquences pour le modèle LSTM
        
        Args:
            data_scaled: Données normalisées
            
        Returns:
            Array 3D pour LSTM
        """
        sequences = []
        
        # Créer fenêtres glissantes
        for i in range(len(data_scaled) - self.window_size + 1):
            sequence = data_scaled[i:i + self.window_size]
            sequences.append(sequence)
        
        return np.array(sequences)
    
    def predict(self, data):
        """
        Prédire le SoH
        
        Args:
            data: DataFrame avec les features brutes
            
        Returns:
            Array de prédictions SoH
        """
        # Prétraiter
        data_scaled = self.preprocess_data(data)
        
        # Créer séquences
        sequences = self.create_sequences(data_scaled)
        
        if len(sequences) == 0:
            raise ValueError(f"Pas assez de données. Minimum requis : {self.window_size} mesures")
        
        # Prédire
        predictions = self.model.predict(sequences, verbose=0)
        
        return predictions.flatten()
    
    def predict_single(self, voltage, current, temperature, soc, cycle):
        """
        Prédire pour une seule mesure (nécessite historique de window_size mesures)
        
        Args:
            voltage, current, temperature, soc, cycle: Listes de valeurs
            
        Returns:
            Prédiction SoH
        """
        # Créer DataFrame
        data = pd.DataFrame({
            'Voltage_measured': voltage,
            'Current_measured': current,
            'Temperature_measured': temperature,
            'SoC': soc,
            'cycle_number': cycle
        })
        
        # Prédire
        predictions = self.predict(data)
        
        return predictions[-1]  # Retourner dernière prédiction


def main():
    """
    Exemple d'utilisation
    """
    print("=" * 70)
    print("🔮 PRÉDICTEUR SoH - BATTERIES")
    print("=" * 70)
    
    # Initialiser
    predictor = BatteryHealthPredictor()
    
    # Exemple : Charger nouvelles données
    print("\n📊 Exemple de prédiction sur nouvelles données...")
    
    # Simuler des données
    n_samples = 25  # Plus que window_size
    example_data = pd.DataFrame({
        'Voltage_measured': np.random.uniform(3.2, 4.2, n_samples),
        'Current_measured': np.random.uniform(-2, 2, n_samples),
        'Temperature_measured': np.random.uniform(20, 35, n_samples),
        'SoC': np.random.uniform(0, 1, n_samples),
        'cycle_number': np.arange(1, n_samples + 1)
    })
    
    # Prédire
    predictions = predictor.predict(example_data)
    
    print(f"\n✅ {len(predictions)} prédictions générées")
    print(f"   SoH moyen prédit : {predictions.mean():.2f}%")
    print(f"   SoH min : {predictions.min():.2f}%")
    print(f"   SoH max : {predictions.max():.2f}%")
    
    print("\n" + "=" * 70)
    print("✅ Prédiction terminée !")
    print("=" * 70)


if __name__ == "__main__":
    main()