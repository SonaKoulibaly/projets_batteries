"""
Point d'entrée principal du projet - Prédiction SoH Batteries
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import après ajout au path
try:
    from predict import BatteryHealthPredictor
except ImportError:
    print("❌ Erreur : Impossible d'importer predict.py")
    print("Vérifiez que src/predict.py existe")
    sys.exit(1)
from predict import BatteryHealthPredictor
import pandas as pd
import numpy as np

def predict_from_file(file_path, model_path='models/lstm_soh_best.h5'):
    """Faire des prédictions à partir d'un fichier CSV"""
    print("=" * 70)
    print("🔮 PRÉDICTION SoH - BATTERIES")
    print("=" * 70)
    
    print(f"\n📂 Chargement : {file_path}")
    data = pd.read_csv(file_path)
    print(f"✅ {len(data)} mesures chargées")
    
    print(f"\n🔧 Chargement du modèle...")
    predictor = BatteryHealthPredictor(model_path=model_path)
    
    print(f"\n🔮 Prédictions...")
    try:
        predictions = predictor.predict(data)
        
        print(f"\n✅ {len(predictions)} prédictions générées !")
        print(f"\n📊 Résultats :")
        print(f"   SoH moyen : {predictions.mean():.2f}%")
        print(f"   SoH min   : {predictions.min():.2f}%")
        print(f"   SoH max   : {predictions.max():.2f}%")
        
        output_path = file_path.replace('.csv', '_predictions.csv')
        pd.DataFrame({'Predicted_SoH': predictions}).to_csv(output_path, index=False)
        print(f"\n💾 Sauvegardé : {output_path}")
        
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        return False
    
    print("=" * 70)
    return True


def demo():
    """Démonstration avec données synthétiques"""
    print("=" * 70)
    print("🎬 MODE DÉMONSTRATION")
    print("=" * 70)
    
    n_samples = 25
    demo_data = pd.DataFrame({
        'Voltage_measured': np.random.uniform(3.2, 4.2, n_samples),
        'Current_measured': np.random.uniform(-2, 2, n_samples),
        'Temperature_measured': np.random.uniform(20, 35, n_samples),
        'SoC': np.linspace(0.1, 0.9, n_samples),
        'cycle_number': np.arange(1, n_samples + 1)
    })
    
    temp_file = 'demo_data.csv'
    demo_data.to_csv(temp_file, index=False)
    
    success = predict_from_file(temp_file)
    
    import os
    if os.path.exists(temp_file): os.remove(temp_file)
    if os.path.exists('demo_data_predictions.csv'): os.remove('demo_data_predictions.csv')
    
    return success


def main():
    parser = argparse.ArgumentParser(description='Prédiction SoH Batteries')
    parser.add_argument('--demo', action='store_true', help='Mode démonstration')
    parser.add_argument('--file', type=str, help='Fichier CSV')
    parser.add_argument('--model', type=str, default='models/lstm_soh_best.h5', help='Modèle')
    
    args = parser.parse_args()
    
    if args.demo:
        success = demo()
    elif args.file:
        success = predict_from_file(args.file, args.model)
    else:
        parser.print_help()
        print("\n⚠️  Spécifiez --demo ou --file")
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())