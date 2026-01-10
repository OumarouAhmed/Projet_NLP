import json
import random
import os

# Chemins des fichiers
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

def augment_products(target_count=1000):
    if not os.path.exists(PRODUCTS_FILE):
        print(f"Erreur : Le fichier {PRODUCTS_FILE} n'existe pas.")
        return

    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        existing_products = json.load(f)

    print(f"Nombre de produits actuels : {len(existing_products)}")
    
    if len(existing_products) >= target_count:
        print("Le nombre cible est déjà atteint ou dépassé.")
        return

    # Listes pour la génération synthétique
    adjectives = ["élégant", "moderne", "vintage", "confortable", "premium", "eco-friendly", "chic", "décontracté", "sportif", "classique", "tendance", "luxueux"]
    materials = ["en coton", "en lin", "en laine", "en soie", "en cuir synthétique", "en denim", "en velours", "en polyester recyclé"]
    brands = ["EcoStyle", "UrbanFit", "LuxeWear", "DailyBasic", "TrendSetters", "NordicDesign", "ModaViva", "PureCotton"]
    
    new_products = list(existing_products)
    
    # Utiliser les produits existants comme templates
    templates = existing_products
    
    while len(new_products) < target_count:
        template = random.choice(templates)
        adj = random.choice(adjectives)
        mat = random.choice(materials)
        brand = random.choice(brands)
        
        # Créer un nouveau nom et une nouvelle description
        new_name = f"{template['name']} {adj} {brand}"
        new_description = f"{template['description']}. Ce modèle {adj} {mat} de la marque {brand} est un incontournable."
        
        # Faire varier légèrement le prix (entre -20% et +40%)
        price_variation = random.uniform(0.8, 1.4)
        new_price = round(template['price'] * price_variation, 2)
        
        # Créer le nouveau produit
        new_product = {
            "name": new_name,
            "category": template['category'],
            "gender": template['gender'],
            "price": new_price,
            "description": new_description,
            "size": template['size'],
            "color": template['color']
        }
        
        # Vérifier l'unicité du nom pour éviter les doublons exacts
        if not any(p['name'] == new_name for p in new_products):
            new_products.append(new_product)

    # Sauvegarder les produits augmentés
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_products, f, ensure_ascii=False, indent=2)
    
    print(f"Succès : Le fichier contient maintenant {len(new_products)} produits.")

if __name__ == "__main__":
    augment_products(1000)
