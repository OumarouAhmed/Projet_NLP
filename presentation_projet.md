# Présentation de Soutenance : Chatbot E-commerce NLP

Ce document est structuré comme une série de slides pour votre présentation.

---

## 📸 Slide 1 : Titre du Projet
**Titre :** Système de Relation Client Automatisé par Intelligence Artificielle (NLP)
**Sous-titre :** Application au secteur de l'E-commerce Mode
**Présenté par :** [Votre Nom]
**Mots-clés :** NLP, Python, Machine Learning, MongoDB, Streamlit

---

## 🎯 Slide 2 : Introduction et Problématique
**Contexte :**
- Explosion de l'e-commerce et besoin de réactivité 24h/24.
- Charge de travail importante pour le support client humain sur des questions répétitives.
**Problématique :**
- Comment automatiser le support client tout en gardant une compréhension naturelle des besoins utilisateur ?
**Objectif :**
- Développer un agent conversationnel capable de comprendre les intentions, de consulter un catalogue produits et de répondre aux FAQ.

---

## 🏗️ Slide 3 : Architecture du Système
**Structure Modulaire :**
1. **Module NLP :** Intelligence du chatbot (Classification d'intention + **Extraction d'entités**).
2. **Module Database :** Stockage persistant (MongoDB).
3. **Module Engine :** Logique métier et génération de réponses.
4. **Interface UX :** Dashboard et Chat (Streamlit).

---

## 🧠 Slide 4 : Pipeline NLP (Le cœur du projet)
**Étapes de traitement du texte :**
1. **Nettoyage :** Suppression de la ponctuation, passage en minuscules.
2. **Tokenisation :** Découpage en mots.
3. **Stop-words :** Retrait des mots vides (le, la, de, etc.).
4. **Lemmatisation/Stemming :** Réduction à la racine des mots pour une meilleure généralisation.

---

## 📉 Slide 5 : Modèle de Machine Learning
**Algorithme :** Logistic Regression (Régression Logistique).
**Vectorisation :** TF-IDF (Term Frequency-Inverse Document Frequency).
**Pourquoi ce choix ?**
- Efficace pour des datasets de petite à moyenne taille.
- Temps d'entraînement et d'inférence très rapide.
- Excellente interprétabilité des résultats.
**Limites :**
- Moins performant sur la sémantique complexe (ironie, double négation) comparé aux Transformers.

---

## 📦 Slide 6 : Gestion des Données (MongoDB)
**Pourquoi MongoDB (NoSQL) ?**
- Flexibilité des schémas (parfait pour des FAQ variées).
- Scalabilité horizontale.
**Données gérées :**
- **Produits :** Catalogue de 1000 articles (générés synthétiquement pour le stress-test).
- **FAQ :** Réponses aux questions de livraison, paiement, retours.
- **Logs :** Historique des conversations.

---

## 🖥️ Slide 7 : Interface Utilisateur (Streamlit)
**Dashboard Analytics :**
- Visualisation en temps réel des performances.
- Distribution des intentions (intent distribution).
- Score de confiance moyen du modèle.
**Interface de Chat :**
- Expérience fluide et interactive.
- Affichage dynamique des résultats de recherche produits.

---

## 🧪 Slide 8 : Démonstration - Scénarios Clés
**Scénario 1 :** Recherche de produits.
*Input :* "Je cherche une robe rouge pour une soirée."
*Action :* Le chatbot identifie l'intention `recherche_produit` **ET** extrait les entités (Produit: "robe", Couleur: "rouge") pour filtrer la base MongoDB.

**Scénario 2 :** Question logistique.
*Input :* "Quels sont les délais de livraison ?"
*Action :* Le chatbot pioche la réponse exacte dans la collection FAQ.

**Gestion des erreurs (Fallback) :**
- Si le score de confiance est faible (< 0.5), le bot répond : *"Je n'ai pas bien compris votre demande. Pouvez-vous reformuler ?"* ou propose de contacter le support humain.

---

## 🚀 Slide 9 : Performances et Analytics
- **Volume de données :** Dataset de 1000 produits et multiples intentions.
- **Vitesse :** Réponse quasi-instantanée (< 100ms).
- **Fiabilité :** Evaluation via matrice de confusion et F1-Score (lors de l'entraînement).

---

## 🔮 Slide 10 : Perspectives d'Amélioration
1. **Modèles Transformers :** Migration vers CamemBERT pour une meilleure compréhension contextuelle.
2. **Analyse de Sentiment :** Détecter la frustration du client pour passer la main à un humain.
3. **Multilingue :** Support de l'anglais et de l'espagnol.

---

## ✅ Slide 11 : Conclusion
**Bilan :**
- Projet complet allant de la collecte de données à l'interface utilisateur.
- Utilisation de technologies modernes et demandées sur le marché (Python/NLP/NoSQL).
- Solution scalable et prête à l'emploi.

**Merci de votre attention ! Avez-vous des questions ?**
