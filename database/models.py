"""
Modèles de données MongoDB
"""
from datetime import datetime
from database.mongodb_connection import mongodb

class ProductModel:
    """Modèle pour les produits"""
    
    @staticmethod
    def get_collection():
        return mongodb.get_collection("products")
    
    @staticmethod
    def insert_product(product_data):
        """Insère un produit"""
        try:
            collection = ProductModel.get_collection()
            product_data["created_at"] = datetime.now()
            return collection.insert_one(product_data)
        except Exception as e:
            print(f"⚠️ Impossible d'insérer le produit: {e}")
            return None
    
    @staticmethod
    def search_products(query, category=None, gender=None, limit=10):
        """Recherche de produits"""
        try:
            collection = ProductModel.get_collection()
            search_filter = {}
            
            if category:
                search_filter["category"] = {"$regex": category, "$options": "i"}
            if gender:
                search_filter["gender"] = {"$regex": gender, "$options": "i"}
            if query:
                search_filter["$or"] = [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            
            return list(collection.find(search_filter).limit(limit))
        except Exception as e:
            print(f"⚠️ Impossible de rechercher les produits: {e}")
            return []
    
    @staticmethod
    def get_all_products():
        """Récupère tous les produits"""
        try:
            collection = ProductModel.get_collection()
            return list(collection.find({}))
        except Exception as e:
            print(f"⚠️ Impossible de récupérer les produits: {e}")
            return []

class ConversationModel:
    """Modèle pour les conversations"""
    
    @staticmethod
    def get_collection():
        import config
        return mongodb.get_collection(config.COLLECTION_NAME)
    
    @staticmethod
    def save_conversation(user_message, bot_response, intent, confidence):
        """Sauvegarde une conversation"""
        try:
            collection = ConversationModel.get_collection()
            conversation = {
                "user_message": user_message,
                "bot_response": bot_response,
                "intent": intent,
                "confidence": confidence,
                "timestamp": datetime.now()
            }
            return collection.insert_one(conversation)
        except Exception as e:
            print(f"⚠️ Impossible de sauvegarder la conversation: {e}")
            return None
    
    @staticmethod
    def get_conversation_stats():
        """Récupère les statistiques des conversations"""
        try:
            collection = ConversationModel.get_collection()
            total = collection.count_documents({})
            
            # Statistiques par intention
            pipeline = [
                {"$group": {"_id": "$intent", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            intent_stats = list(collection.aggregate(pipeline))
            
            # Conversations récentes
            recent = list(collection.find().sort("timestamp", -1).limit(10))
            
            return {
                "total_conversations": total,
                "intent_distribution": intent_stats,
                "recent_conversations": recent
            }
        except Exception as e:
            print(f"⚠️ Impossible de récupérer les statistiques: {e}")
            return {
                "total_conversations": 0,
                "intent_distribution": [],
                "recent_conversations": []
            }

class FAQModel:
    """Modèle pour la FAQ"""
    
    @staticmethod
    def get_collection():
        return mongodb.get_collection("faq")
    
    @staticmethod
    def insert_faq(faq_data):
        """Insère une FAQ"""
        try:
            collection = FAQModel.get_collection()
            faq_data["created_at"] = datetime.now()
            return collection.insert_one(faq_data)
        except Exception as e:
            print(f"⚠️ Impossible d'insérer la FAQ: {e}")
            return None
    
    @staticmethod
    def get_faq_by_intent(intent):
        """Récupère la FAQ par intention"""
        try:
            collection = FAQModel.get_collection()
            return collection.find_one({"intent": intent})
        except Exception as e:
            print(f"⚠️ Impossible de récupérer la FAQ: {e}")
            return None
    
    @staticmethod
    def get_all_faq():
        """Récupère toutes les FAQ"""
        try:
            collection = FAQModel.get_collection()
            return list(collection.find({}))
        except Exception as e:
            print(f"⚠️ Impossible de récupérer les FAQ: {e}")
            return []

