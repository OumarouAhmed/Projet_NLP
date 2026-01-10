# 🚀 Guide de Démarrage Rapide

## Prérequis

- Python 3.8 ou supérieur
- MongoDB installé et en cours d'exécution (local ou cloud)
- pip (gestionnaire de paquets Python)

## Installation Rapide

### Étape 1 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 2 : Installer le modèle spaCy français

```bash
python -m spacy download fr_core_news_sm
```

### Étape 3 : Configurer MongoDB

Créez un fichier `.env` à la racine du projet :

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=chatbot_commerce
COLLECTION_NAME=chatbot_commerce
```

**Pour MongoDB Atlas (cloud)** :
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=chatbot_commerce
COLLECTION_NAME=chatbot_commerce
```

### Étape 4 : Initialiser la base de données

```bash
python scripts/init_database.py
```

Cette commande va :
- ✅ Créer les collections MongoDB
- ✅ Insérer les produits depuis `data/products.json`
- ✅ Insérer la FAQ depuis `data/faq.json`

### Étape 5 : Entraîner le modèle

```bash
python scripts/train_model.py
```

Cette commande va :
- ✅ Charger les données d'entraînement
- ✅ Entraîner le classificateur d'intentions
- ✅ Sauvegarder le modèle dans `models/`

**Temps estimé :** 1-2 minutes

### Étape 6 : Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible à : **http://localhost:8501**

## 🎯 Utilisation

### Interface Chat

1. Accédez à la page **💬 Chat**
2. Tapez votre question
3. Le chatbot répond automatiquement

### Exemples de questions

- "Bonjour"
- "Montre-moi les robes"
- "Combien de temps prend la livraison ?"
- "Quels modes de paiement acceptez-vous ?"
- "Comment retourner un article ?"
- "Y a-t-il des soldes ?"

### Dashboard

- **📊 Dashboard** : Statistiques et analytics
- **📦 Produits** : Recherche et gestion des produits
- **⚙️ Configuration** : État du système

## 🔧 Dépannage

### Erreur : "Modèle non trouvé"

**Solution :** Exécutez `python scripts/train_model.py`

### Erreur : "MongoDB non connecté"

**Solutions :**
1. Vérifiez que MongoDB est en cours d'exécution
2. Vérifiez votre URI dans `.env`
3. Testez la connexion : `mongosh` ou `mongo`

### Erreur : "Module spaCy non trouvé"

**Solution :** 
```bash
python -m spacy download fr_core_news_sm
```

### Erreur : "NLTK data not found"

**Solution :** Le script télécharge automatiquement les données nécessaires. Si le problème persiste :
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 📝 Structure des Données

### Ajouter des produits

Éditez `data/products.json` ou utilisez MongoDB directement.

### Ajouter des exemples d'entraînement

Éditez `data/training_data.json` pour améliorer la reconnaissance d'intentions.

### Modifier les réponses

Éditez `chatbot/response_generator.py` pour personnaliser les réponses.

## 🎓 Prochaines Étapes

1. **Personnaliser les données** : Ajoutez vos propres produits et FAQ
2. **Améliorer le modèle** : Ajoutez plus d'exemples d'entraînement
3. **Déployer** : Utilisez Streamlit Cloud ou un serveur dédié

## 📞 Support

Pour toute question, consultez le `README.md` ou les commentaires dans le code.

