# 🤖 Chatbot Intelligent de Support Client - E-commerce Mode

Un chatbot conversationnel intelligent développé avec Python pour assister les clients d'un site e-commerce de vêtements. Le projet utilise des techniques de Traitement Automatique du Langage Naturel (NLP) pour comprendre les intentions des utilisateurs et générer des réponses adaptées.

## 📋 Fonctionnalités

### Fonctionnalités Principales

1. **Recherche de produits** : "Montre-moi les robes d'été" / "Avez-vous des chemises pour hommes ?"
2. **Livraison et suivi** : "Combien de temps prend la livraison ?" / "Comment suivre ma commande ?"
3. **Paiement et retours** : "Quels modes de paiement acceptez-vous ?" / "Comment retourner un article ?"
4. **Promotions et nouveautés** : "Y a-t-il des soldes aujourd'hui ?" / "Quels sont les nouveaux produits ?"
5. **Assistance générale** : "Quels sont vos horaires ?" / "Comment vous contacter ?"

### Interface Dashboard

- **💬 Chat** : Interface de conversation avec le chatbot
- **📊 Dashboard** : Statistiques et analytics des conversations
- **📦 Produits** : Gestion et recherche de produits
- **⚙️ Configuration** : Paramètres et état du système

## 🛠️ Stack Technologique

- **Python 3.8+**
- **NLTK / spaCy** : Prétraitement et analyse du langage naturel
- **scikit-learn** : Classification d'intentions (TF-IDF + Logistic Regression)
- **Streamlit** : Interface utilisateur web
- **MongoDB** : Base de données pour produits, FAQ et conversations
- **pymongo** : Connexion MongoDB
- **Plotly** : Visualisations dans le dashboard

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd Projet_NLP
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Installer le modèle spaCy français

```bash
python -m spacy download fr_core_news_sm
```

### 4. Configuration MongoDB

Créez un fichier `.env` à la racine du projet :

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=chatbot_commerce
COLLECTION_NAME=chatbot_commerce
```

Ou modifiez directement `config.py` avec vos paramètres MongoDB.

### 5. Initialiser la base de données

```bash
python scripts/init_database.py
```

Cette commande va :
- Créer les collections MongoDB
- Insérer les produits depuis `data/products.json`
- Insérer la FAQ depuis `data/faq.json`

### 6. Entraîner le modèle

```bash
python scripts/train_model.py
```

Cette commande va :
- Charger les données d'entraînement depuis `data/training_data.json`
- Entraîner le classificateur d'intentions
- Sauvegarder le modèle dans `models/`

## 🚀 Utilisation

### Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Utilisation du Chatbot

1. Accédez à la page **💬 Chat**
2. Tapez votre question dans la zone de saisie
3. Le chatbot analysera votre intention et générera une réponse adaptée

### Exemples de questions

- "Bonjour"
- "Montre-moi les robes"
- "Combien de temps prend la livraison ?"
- "Quels modes de paiement acceptez-vous ?"
- "Comment retourner un article ?"
- "Y a-t-il des soldes ?"
- "Comment vous contacter ?"

## 📁 Structure du Projet

```
Projet_NLP/
├── app.py                      # Application Streamlit principale
├── config.py                   # Configuration du projet
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── .env                        # Variables d'environnement (à créer)
│
├── chatbot/                    # Module chatbot
│   ├── chatbot_engine.py      # Moteur principal
│   └── response_generator.py   # Générateur de réponses
│
├── nlp/                        # Module NLP
│   ├── preprocessing.py        # Prétraitement du texte
│   └── intent_classifier.py    # Classification d'intentions
│
├── database/                   # Module base de données
│   ├── mongodb_connection.py   # Connexion MongoDB
│   └── models.py              # Modèles de données
│
├── data/                       # Données
│   ├── training_data.json     # Données d'entraînement
│   ├── products.json          # Catalogue produits
│   └── faq.json               # FAQ
│
├── scripts/                    # Scripts utilitaires
│   ├── train_model.py         # Entraînement du modèle
│   └── init_database.py       # Initialisation MongoDB
│
└── models/                     # Modèles sauvegardés (généré)
    ├── intent_classifier.pkl
    └── tfidf_vectorizer.pkl
```

## 🧠 Architecture NLP

### Pipeline de Traitement

1. **Prétraitement** :
   - Nettoyage du texte (minuscules, suppression caractères spéciaux)
   - Tokenisation
   - Suppression des stopwords
   - Stemming (racinisation)

2. **Vectorisation** :
   - TF-IDF (Term Frequency-Inverse Document Frequency)
   - N-grammes (1-2)

3. **Classification** :
   - Logistic Regression (multinomial)
   - Classification multi-classes

### Intentions Supportées

- `salutation` : Accueil
- `au_revoir` : Départ
- `recherche_produit` : Recherche de produits
- `livraison` : Questions sur la livraison
- `paiement` : Questions sur le paiement
- `retour` : Questions sur les retours
- `promotion` : Questions sur les promotions
- `contact` : Coordonnées et horaires

## 📊 Dashboard Analytics

Le dashboard affiche :
- Nombre total de conversations
- Confiance moyenne des prédictions
- Distribution des intentions (graphique)
- Conversations récentes
- Statistiques par intention

## 🔧 Configuration Avancée

### Modifier les données d'entraînement

Éditez `data/training_data.json` pour ajouter/modifier des exemples d'intentions.

### Ajouter des produits

Éditez `data/products.json` ou utilisez l'API MongoDB pour ajouter des produits.

### Personnaliser les réponses

Modifiez `chatbot/response_generator.py` pour personnaliser les réponses du chatbot.

## 🧪 Évaluation

Le modèle est évalué avec :
- Précision (accuracy)
- Rapport de classification (precision, recall, F1-score)
- Matrice de confusion

## 🚀 Améliorations Futures

- [ ] Intégration de modèles Transformer (BERT français)
- [ ] Apprentissage continu (fine-tuning)
- [ ] Intégration vocale (speech-to-text)
- [ ] Support multilingue
- [ ] Analyse de sentiment
- [ ] Recommandations personnalisées
- [ ] API REST pour intégration externe

## 📝 Licence

Ce projet est un projet éducatif.

## 👥 Auteur

Projet développé dans le cadre d'un projet NLP.

## 📚 Ressources

- [NLTK Documentation](https://www.nltk.org/)
- [spaCy Documentation](https://spacy.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MongoDB Documentation](https://docs.mongodb.com/)

