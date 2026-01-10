"""
Script d'initialisation de la base de données MongoDB
"""
import json
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import ProductModel, FAQModel
import config

def load_json_data(file_path):
    """Charge les données depuis un fichier JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def init_products():
    """Initialise les produits dans MongoDB"""
    print("📦 Initialisation des produits...")
    products = load_json_data(config.PRODUCTS_DATA_PATH)
    collection = ProductModel.get_collection()
    
    # Vider la collection si elle existe
    collection.delete_many({})
    
    # Insérer les produits
    for product in products:
        ProductModel.insert_product(product)
    
    print(f"✅ {len(products)} produits insérés")

def init_faq():
    """Initialise la FAQ dans MongoDB"""
    print("❓ Initialisation de la FAQ...")
    faq_items = load_json_data(config.FAQ_DATA_PATH)
    collection = FAQModel.get_collection()
    
    # Vider la collection si elle existe
    collection.delete_many({})
    
    # Insérer les FAQ
    for faq in faq_items:
        FAQModel.insert_faq(faq)
    
    print(f"✅ {len(faq_items)} entrées FAQ insérées")

def main():
    """Fonction principale"""
    print("🚀 Initialisation de la base de données MongoDB...")
    print("=" * 50)
    
    try:
        init_products()
        init_faq()
        
        print("\n" + "=" * 50)
        print("✅ Base de données initialisée avec succès !")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        raise

if __name__ == "__main__":
    main()


