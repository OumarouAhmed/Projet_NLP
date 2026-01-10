"""
Script d'entraînement du modèle de classification d'intentions
"""
import json
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.intent_classifier import IntentClassifier
import config

def load_training_data():
    """Charge les données d'entraînement"""
    with open(config.TRAINING_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Fonction principale"""
    print("🚀 Démarrage de l'entraînement du modèle...")
    print("=" * 50)
    
    # Charger les données
    print(f"📂 Chargement des données depuis {config.TRAINING_DATA_PATH}")
    training_data = load_training_data()
    
    # Créer et entraîner le classificateur
    classifier = IntentClassifier()
    accuracy = classifier.train(training_data)
    
    # Sauvegarder le modèle
    print("\n💾 Sauvegarde du modèle...")
    classifier.save()
    
    print("\n" + "=" * 50)
    print(f"✅ Entraînement terminé avec une précision de {accuracy:.2%}")
    print("=" * 50)

if __name__ == "__main__":
    main()


