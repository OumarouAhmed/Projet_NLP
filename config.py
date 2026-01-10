"""
Configuration du projet
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "chatbot_commerce")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "chatbot_commerce")

# Configuration NLP
MODEL_PATH = "models/intent_classifier.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"
SPACY_MODEL = "fr_core_news_sm"

# Configuration des données
DATA_DIR = "data"
TRAINING_DATA_PATH = os.path.join(DATA_DIR, "training_data.json")
PRODUCTS_DATA_PATH = os.path.join(DATA_DIR, "products.json")
FAQ_DATA_PATH = os.path.join(DATA_DIR, "faq.json")

# Intentions supportées
INTENTS = [
    "recherche_produit",
    "livraison",
    "paiement",
    "retour",
    "promotion",
    "contact",
    "salutation",
    "au_revoir"
]

