"""
Tests unitaires pour le preprocessing
"""

import unittest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils import create_sliding_windows, calculate_metrics


class TestPreprocessing(unittest.TestCase):
    """Tests pour les fonctions de preprocessing"""
    
    def setUp(self):
        """Préparer les données de test"""
        # Créer un petit dataset simulé
        self.test_data = pd.DataFrame({
            'Voltage_measured': [3.5, 3.6, 3.7, 3.8, 3.9, 4.0] * 2,
            'Current_measured': [1.0, 1.1, 1.2, 1.1, 1.0, 0.9] * 2,
            'Temperature_measured': [25, 26, 27, 26, 25, 24] * 2,
            'SoC': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7] * 2,
            'cycle_number': [1, 2, 3, 4, 5, 6] * 2,
            'battery_id': ['B1']*6 + ['B2']*6,
            'SoH': [90, 89, 88, 87, 86, 85] * 2
        })
        
        self.feature_cols = ['Voltage_measured', 'Current_measured', 
                            'Temperature_measured', 'SoC', 'cycle_number']
    
    def test_sliding_windows_shape(self):
        """Tester que create_sliding_windows retourne les bonnes dimensions"""
        window_size = 3
        
        X, y, ids = create_sliding_windows(
            self.test_data, 
            window_size=window_size,
            feature_cols=self.feature_cols
        )
        
        # Vérifier les dimensions
        self.assertEqual(len(X.shape), 3)  # 3D array
        self.assertEqual(X.shape[1], window_size)  # Timesteps
        self.assertEqual(X.shape[2], len(self.feature_cols))  # Features
        self.assertEqual(len(y), len(X))  # Même nombre d'échantillons
        self.assertEqual(len(ids), len(X))  # IDs pour chaque échantillon
    
    def test_sliding_windows_values(self):
        """Tester que les valeurs sont correctement extraites"""
        window_size = 3
        
        X, y, ids = create_sliding_windows(
            self.test_data, 
            window_size=window_size,
            feature_cols=self.feature_cols
        )
        
        # Vérifier que y contient bien des valeurs de SoH
        self.assertTrue(np.all(y >= 0))
        self.assertTrue(np.all(y <= 100))
    
    def test_calculate_metrics(self):
        """Tester le calcul des métriques"""
        y_true = np.array([80, 85, 90, 75, 70])
        y_pred = np.array([82, 84, 89, 76, 72])
        
        metrics = calculate_metrics(y_true, y_pred)
        
        # Vérifier que toutes les métriques sont présentes
        self.assertIn('mae', metrics)
        self.assertIn('rmse', metrics)
        self.assertIn('r2', metrics)
        self.assertIn('mape', metrics)
        
        # Vérifier que les valeurs sont raisonnables
        self.assertGreaterEqual(metrics['mae'], 0)
        self.assertGreaterEqual(metrics['rmse'], 0)
        self.assertLessEqual(metrics['r2'], 1)
    
    def test_metrics_perfect_prediction(self):
        """Tester métriques avec prédiction parfaite"""
        y_true = np.array([80, 85, 90, 75, 70])
        y_pred = y_true.copy()
        
        metrics = calculate_metrics(y_true, y_pred)
        
        # MAE et RMSE devraient être 0
        self.assertAlmostEqual(metrics['mae'], 0, places=5)
        self.assertAlmostEqual(metrics['rmse'], 0, places=5)
        
        # R² devrait être 1
        self.assertAlmostEqual(metrics['r2'], 1.0, places=5)
    
    def test_window_size_too_large(self):
        """Tester avec window_size trop grand"""
        window_size = 100  # Plus grand que les données
        
        X, y, ids = create_sliding_windows(
            self.test_data, 
            window_size=window_size,
            feature_cols=self.feature_cols
        )
        
        # Devrait retourner des arrays vides
        self.assertEqual(len(X), 0)
        self.assertEqual(len(y), 0)


class TestDataValidation(unittest.TestCase):
    """Tests pour la validation des données"""
    
    def test_missing_values(self):
        """Tester détection de valeurs manquantes"""
        data = pd.DataFrame({
            'Voltage_measured': [3.5, np.nan, 3.7],
            'SoH': [90, 89, 88]
        })
        
        # Vérifier qu'il y a des NaN
        self.assertTrue(data.isnull().any().any())
    
    def test_soh_range(self):
        """Tester que SoH est dans la plage 0-100"""
        data = pd.DataFrame({
            'SoH': [50, 75, 90, 105]  # 105 est invalide
        })
        
        invalid = data[data['SoH'] > 100]
        self.assertGreater(len(invalid), 0)


def run_tests():
    """Exécuter tous les tests"""
    # Créer une suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    
    # Exécuter
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 70)
    print("🧪 TESTS UNITAIRES - PREPROCESSING")
    print("=" * 70)
    
    success = run_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ TOUS LES TESTS RÉUSSIS !")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print("=" * 70)