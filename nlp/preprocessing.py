"""
Module de prétraitement NLP
"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import spacy

# Téléchargement des ressources NLTK nécessaires
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class TextPreprocessor:
    """Classe pour le prétraitement du texte"""
    
    def __init__(self):
        self.stemmer = SnowballStemmer('french')
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except OSError:
            # Fallback for environments without the model package.
            print("spaCy model 'fr_core_news_sm' not found; using blank 'fr' model.")
            self.nlp = spacy.blank("fr")
        # Stopwords français
        try:
            self.stop_words = set(stopwords.words('french'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('french'))
    
    def clean_text(self, text):
        """Nettoie le texte"""
        if not text:
            return ""
        
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères spéciaux (garder les accents)
        text = re.sub(r'[^a-zàâäéèêëïîôöùûüÿç\s]', '', text)
        
        # Suppression des espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize(self, text):
        """Tokenise le texte"""
        try:
            tokens = word_tokenize(text, language='french')
            return tokens
        except:
            return text.split()
    
    def remove_stopwords(self, tokens):
        """Supprime les stopwords"""
        return [token for token in tokens if token not in self.stop_words]
    
    def stem(self, tokens):
        """Applique le stemming"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess(self, text, remove_stopwords=True, apply_stemming=True):
        """Pipeline complet de prétraitement"""
        # Nettoyage
        cleaned = self.clean_text(text)
        
        # Tokenisation
        tokens = self.tokenize(cleaned)
        
        # Suppression des stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Stemming
        if apply_stemming:
            tokens = self.stem(tokens)
        
        return ' '.join(tokens)
    
    def extract_entities(self, text):
        """Extrait les entités nommées avec spaCy"""
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        
        return entities

# Instance globale
preprocessor = TextPreprocessor()


