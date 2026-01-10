"""
Script de test du chatbot
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.chatbot_engine import ChatbotEngine

def test_chatbot():
    """Test basique du chatbot"""
    print("🧪 Test du Chatbot")
    print("=" * 50)
    
    try:
        chatbot = ChatbotEngine()
        
        # Tests avec différentes intentions
        test_messages = [
            "bonjour",
            "montre moi les robes",
            "combien de temps prend la livraison",
            "quels modes de paiement acceptez vous",
            "comment retourner un article",
            "y a t il des soldes",
            "au revoir"
        ]
        
        print("\n📝 Tests de classification d'intentions:\n")
        
        for message in test_messages:
            try:
                response = chatbot.process_message(message)
                print(f"💬 Message: {message}")
                print(f"   Intention: {response['intent']}")
                print(f"   Confiance: {response['confidence']:.2%}")
                print(f"   Réponse: {response['response'][:100]}...")
                print()
            except Exception as e:
                print(f"❌ Erreur pour '{message}': {e}")
                print()
        
        print("=" * 50)
        print("✅ Tests terminés")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print("\n💡 Vérifiez que:")
        print("   1. Le modèle a été entraîné (python scripts/train_model.py)")
        print("   2. MongoDB est connecté")
        print("   3. La base de données a été initialisée (python scripts/init_database.py)")

if __name__ == "__main__":
    test_chatbot()


