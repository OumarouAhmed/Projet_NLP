"""
Module de classification des intentions
"""
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import config
from nlp.preprocessing import preprocessor

class IntentClassifier:
    """Classificateur d'intentions"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        self.classifier = LogisticRegression(
            max_iter=1000,
            random_state=42
        )
        self.is_trained = False
    
    def prepare_data(self, training_data):
        """Prépare les données d'entraînement"""
        texts = []
        labels = []
        
        for item in training_data:
            intent = item.get('intent')
            examples = item.get('examples', [])
            
            for example in examples:
                # Prétraitement
                processed = preprocessor.preprocess(example)
                texts.append(processed)
                labels.append(intent)
        
        return texts, labels
    
    def train(self, training_data):
        """Entraîne le modèle"""
        print("🔄 Préparation des données...")
        texts, labels = self.prepare_data(training_data)
        
        if len(texts) == 0:
            raise ValueError("Aucune donnée d'entraînement trouvée")
        
        print(f"📊 {len(texts)} exemples d'entraînement")
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print("🔄 Vectorisation TF-IDF...")
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)
        
        print("🔄 Entraînement du classificateur...")
        self.classifier.fit(X_train_vectorized, y_train)
        
        # Évaluation
        y_pred = self.classifier.predict(X_test_vectorized)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Précision du modèle: {accuracy:.2%}")
        print("\n📊 Rapport de classification:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        self.is_trained = True
        return accuracy
    
    def predict(self, text):
        """Prédit l'intention d'un texte"""
        if not self.is_trained:
            raise ValueError("Le modèle n'a pas été entraîné")
        
        # Prétraitement
        processed = preprocessor.preprocess(text)
        
        # Vectorisation
        vectorized = self.vectorizer.transform([processed])
        
        # Prédiction
        intent = self.classifier.predict(vectorized)[0]
        probabilities = self.classifier.predict_proba(vectorized)[0]
        
        # Confiance
        confidence = max(probabilities)
        
        return intent, confidence
    
    def save(self, model_path=None, vectorizer_path=None):
        """Sauvegarde le modèle"""
        model_path = model_path or config.MODEL_PATH
        vectorizer_path = vectorizer_path or config.VECTORIZER_PATH
        
        # Créer le dossier models s'il n'existe pas
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.classifier, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"✅ Modèle sauvegardé: {model_path}")
        print(f"✅ Vectoriseur sauvegardé: {vectorizer_path}")
    
    def load(self, model_path=None, vectorizer_path=None):
        """Charge le modèle"""
        model_path = model_path or config.MODEL_PATH
        vectorizer_path = vectorizer_path or config.VECTORIZER_PATH
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise FileNotFoundError("Modèle non trouvé. Veuillez d'abord entraîner le modèle.")
        
        with open(model_path, 'rb') as f:
            self.classifier = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        self.is_trained = True
        print(f"✅ Modèle chargé: {model_path}")

