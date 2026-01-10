"""
Moteur principal du chatbot
"""
from nlp.intent_classifier import IntentClassifier
from chatbot.response_generator import ResponseGenerator
from database.models import ConversationModel
import config

class ChatbotEngine:
    """Moteur principal du chatbot"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.response_generator = ResponseGenerator()
        self.conversation_model = ConversationModel()
        
        # Charger le modèle si disponible
        try:
            self.intent_classifier.load()
        except FileNotFoundError:
            print("⚠️ Modèle non trouvé. Veuillez d'abord entraîner le modèle.")
    
    def process_message(self, user_message):
        """Traite un message utilisateur et retourne une réponse"""
        if not user_message or not user_message.strip():
            return {
                "response": "Je n'ai pas compris votre message. Pouvez-vous reformuler ?",
                "intent": "unknown",
                "confidence": 0.0
            }
        
        try:
            # Classification de l'intention
            intent, confidence = self.intent_classifier.predict(user_message)
            
            # Génération de la réponse
            response_data = self.response_generator.generate_response(
                intent, user_message, confidence
            )
            
            # Sauvegarde de la conversation
            self.conversation_model.save_conversation(
                user_message=user_message,
                bot_response=response_data.get("response", ""),
                intent=intent,
                confidence=float(confidence)
            )
            
            return {
                "response": response_data.get("response", ""),
                "intent": intent,
                "confidence": float(confidence),
                "type": response_data.get("type", "text"),
                "products": response_data.get("products", [])
            }
        
        except Exception as e:
            print(f"❌ Erreur lors du traitement: {e}")
            return {
                "response": "Désolé, une erreur s'est produite. Pouvez-vous réessayer ?",
                "intent": "error",
                "confidence": 0.0
            }


