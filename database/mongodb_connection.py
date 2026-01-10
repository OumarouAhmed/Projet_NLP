"""
Module de connexion MongoDB
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import config

class MongoDBConnection:
    """Gestionnaire de connexion MongoDB"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self._connected = False
    
    def connect(self):
        """Établit la connexion à MongoDB"""
        if self._connected and self.client:
            return True
        
        try:
            self.client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[config.DATABASE_NAME]
            # Test de connexion
            self.client.admin.command('ping')
            self._connected = True
            print(f"✅ Connexion MongoDB réussie: {config.DATABASE_NAME}")
            return True
        except ConnectionFailure as e:
            self._connected = False
            print(f"⚠️ Erreur de connexion MongoDB: {e}")
            print(f"💡 Vérifiez que MongoDB est en cours d'exécution sur {config.MONGODB_URI}")
            print(f"💡 Vérifiez que la base de données '{config.DATABASE_NAME}' est accessible")
            return False
        except Exception as e:
            self._connected = False
            print(f"⚠️ Erreur de connexion MongoDB: {e}")
            print(f"💡 URI MongoDB: {config.MONGODB_URI}")
            print(f"💡 Base de données: {config.DATABASE_NAME}")
            return False
    
    def get_collection(self, collection_name):
        """Récupère une collection"""
        if not self._connected:
            if not self.connect():
                raise ConnectionError(
                    f"MongoDB n'est pas connecté. "
                    f"URI: {config.MONGODB_URI}, "
                    f"Database: {config.DATABASE_NAME}"
                )
        if not self._connected:
            raise ConnectionError("MongoDB n'est pas connecté")
        return self.db[collection_name]
    
    def is_connected(self):
        """Vérifie si la connexion est active"""
        if not self._connected:
            return self.connect()
        try:
            self.client.admin.command('ping')
            return True
        except:
            self._connected = False
            return False
    
    def close(self):
        """Ferme la connexion"""
        if self.client:
            self.client.close()
            self._connected = False

# Instance globale (connexion lazy - ne se connecte pas automatiquement)
# La connexion se fera uniquement lors du premier appel à get_collection() ou connect()
mongodb = MongoDBConnection()
