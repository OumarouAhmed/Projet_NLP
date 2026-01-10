"""
Générateur de réponses du chatbot
"""
import re
from database.models import ProductModel, FAQModel
from nlp.preprocessing import preprocessor

class ResponseGenerator:
    """Générateur de réponses contextuelles"""
    
    def __init__(self):
        self.product_model = ProductModel()
        self.faq_model = FAQModel()
    
    def extract_product_keywords(self, text):
        """Extrait les mots-clés de recherche de produits"""
        keywords = {
            'category': None,
            'gender': None,
            'query': None
        }
        
        text_lower = text.lower()
        
        # Catégories
        categories = {
            'robe': 'robe',
            'robes': 'robe',
            'chemise': 'chemise',
            'chemises': 'chemise',
            'pantalon': 'pantalon',
            'pantalons': 'pantalon',
            't-shirt': 't-shirt',
            'tshirt': 't-shirt',
            'veste': 'veste',
            'vestes': 'veste',
            'chaussure': 'chaussure',
            'chaussures': 'chaussure',
            'jupe': 'jupe',
            'jupes': 'jupe',
            'pull': 'pull',
            'pulls': 'pull',
            'manteau': 'manteau',
            'manteaux': 'manteau'
        }
        
        for word, category in categories.items():
            if word in text_lower:
                keywords['category'] = category
                break
        
        # Genre
        if any(word in text_lower for word in ['homme', 'hommes', 'masculin', 'pour homme']):
            keywords['gender'] = 'homme'
        elif any(word in text_lower for word in ['femme', 'femmes', 'féminin', 'pour femme']):
            keywords['gender'] = 'femme'
        
        # Mots-clés de recherche
        query_words = []
        for word in text.split():
            if word.lower() not in ['montre', 'moi', 'avez', 'vous', 'des', 'les', 'de', 'la', 'le']:
                query_words.append(word)
        
        if query_words:
            keywords['query'] = ' '.join(query_words)
        
        return keywords
    
    def generate_response(self, intent, user_message, confidence):
        """Génère une réponse selon l'intention"""
        
        if intent == "salutation":
            return self._handle_salutation()
        
        elif intent == "au_revoir":
            return self._handle_au_revoir()
        
        elif intent == "recherche_produit":
            return self._handle_product_search(user_message)
        
        elif intent == "livraison":
            return self._handle_delivery()
        
        elif intent == "paiement":
            return self._handle_payment()
        
        elif intent == "retour":
            return self._handle_return()
        
        elif intent == "promotion":
            return self._handle_promotion()
        
        elif intent == "contact":
            return self._handle_contact()
        
        else:
            return self._handle_unknown()
    
    def _handle_salutation(self):
        return {
            "response": "Bonjour ! 👋 Je suis votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?",
            "type": "text"
        }
    
    def _handle_au_revoir(self):
        return {
            "response": "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions. À bientôt ! 👋",
            "type": "text"
        }
    
    def _handle_product_search(self, user_message):
        """Gère la recherche de produits"""
        keywords = self.extract_product_keywords(user_message)
        
        products = self.product_model.search_products(
            query=keywords['query'],
            category=keywords['category'],
            gender=keywords['gender'],
            limit=5
        )
        
        if products:
            response_text = "Voici quelques produits qui pourraient vous intéresser :\n\n"
            for i, product in enumerate(products, 1):
                response_text += f"{i}. **{product.get('name', 'Produit sans nom')}**\n"
                response_text += f"   - Prix: {product.get('price', 'N/A')}€\n"
                response_text += f"   - Catégorie: {product.get('category', 'N/A')}\n"
                if product.get('description'):
                    desc = product['description'][:100] + "..." if len(product.get('description', '')) > 100 else product['description']
                    response_text += f"   - {desc}\n"
                response_text += "\n"
            
            response_text += "Souhaitez-vous plus de détails sur un produit en particulier ?"
            
            return {
                "response": response_text,
                "type": "products",
                "products": products
            }
        else:
            return {
                "response": "Je n'ai pas trouvé de produits correspondant à votre recherche. Pouvez-vous être plus précis ? Par exemple : 'Montre-moi les robes d'été' ou 'Avez-vous des chemises pour hommes ?'",
                "type": "text"
            }
    
    def _handle_delivery(self):
        faq = self.faq_model.get_faq_by_intent("livraison")
        if faq:
            return {
                "response": faq.get('answer', self._default_delivery_response()),
                "type": "text"
            }
        return {
            "response": self._default_delivery_response(),
            "type": "text"
        }
    
    def _default_delivery_response(self):
        return """📦 **Informations sur la livraison :**

• **Délai de livraison** : 3-5 jours ouvrés en France métropolitaine
• **Frais de livraison** : Gratuits à partir de 50€ d'achat, sinon 4.99€
• **Suivi de commande** : Vous recevrez un email avec un numéro de suivi dès l'expédition
• **Points relais** : Livraison disponible dans plus de 10 000 points relais

Pour suivre votre commande, utilisez le numéro de suivi reçu par email ou connectez-vous à votre compte."""
    
    def _handle_payment(self):
        faq = self.faq_model.get_faq_by_intent("paiement")
        if faq:
            return {
                "response": faq.get('answer', self._default_payment_response()),
                "type": "text"
            }
        return {
            "response": self._default_payment_response(),
            "type": "text"
        }
    
    def _default_payment_response(self):
        return """💳 **Modes de paiement acceptés :**

• Carte bancaire (Visa, Mastercard, American Express)
• PayPal
• Virement bancaire
• Chèque (uniquement pour les commandes supérieures à 50€)

Tous les paiements sont sécurisés via notre système de cryptage SSL."""
    
    def _handle_return(self):
        faq = self.faq_model.get_faq_by_intent("retour")
        if faq:
            return {
                "response": faq.get('answer', self._default_return_response()),
                "type": "text"
            }
        return {
            "response": self._default_return_response(),
            "type": "text"
        }
    
    def _default_return_response(self):
        return """↩️ **Politique de retour :**

• **Délai** : Vous avez 30 jours pour retourner un article
• **Condition** : Articles non portés, avec étiquettes et dans leur emballage d'origine
• **Processus** : 
  1. Connectez-vous à votre compte
  2. Allez dans "Mes commandes"
  3. Sélectionnez l'article à retourner
  4. Imprimez l'étiquette de retour (frais de retour offerts)
  5. Déposez le colis dans un point relais

Le remboursement sera effectué sous 5-7 jours ouvrés après réception."""
    
    def _handle_promotion(self):
        faq = self.faq_model.get_faq_by_intent("promotion")
        if faq:
            return {
                "response": faq.get('answer', self._default_promotion_response()),
                "type": "text"
            }
        return {
            "response": self._default_promotion_response(),
            "type": "text"
        }
    
    def _default_promotion_response(self):
        return """🎉 **Promotions actuelles :**

• **Soldes d'hiver** : Jusqu'à -50% sur une sélection d'articles
• **Nouveautés** : Découvrez notre nouvelle collection printemps-été
• **Code promo** : Utilisez le code WELCOME10 pour 10% de réduction sur votre première commande

Consultez notre page "Promotions" pour voir tous les articles en solde !"""
    
    def _handle_contact(self):
        faq = self.faq_model.get_faq_by_intent("contact")
        if faq:
            return {
                "response": faq.get('answer', self._default_contact_response()),
                "type": "text"
            }
        return {
            "response": self._default_contact_response(),
            "type": "text"
        }
    
    def _default_contact_response(self):
        return """📞 **Nous contacter :**

• **Email** : contact@ecommerce-mode.fr
• **Téléphone** : 01 23 45 67 89 (Lun-Ven, 9h-18h)
• **Chat en direct** : Disponible sur le site (Lun-Ven, 9h-18h)
• **Adresse** : 123 Rue de la Mode, 75001 Paris

**Horaires d'ouverture** : 
- Lundi au Vendredi : 9h - 18h
- Samedi : 10h - 16h
- Dimanche : Fermé"""
    
    def _handle_unknown(self):
        return {
            "response": "Je n'ai pas bien compris votre demande. Pouvez-vous reformuler ? Je peux vous aider avec :\n• La recherche de produits\n• Les livraisons\n• Les paiements\n• Les retours\n• Les promotions\n• Nos coordonnées",
            "type": "text"
        }


