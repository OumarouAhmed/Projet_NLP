# 🎓 Guide de Démonstration Live (Pour le Professeur)

Ce guide vous aide à faire une démonstration sans accroc.

## 🛠️ Avant de commencer
1. Assurez-vous que MongoDB est lancé.
2. Vérifiez que l'application est bien lancée : `streamlit run app.py`.
3. Réinitialisez la page pour avoir un chat vide.

## 📝 Script de la démo

### Étape 1 : Accueil et Salutation
*   **Action :** Tapez "Bonjour"
*   **Ce qu'il faut dire :** "Le chatbot commence par identifier l'intention de salutation grâce au modèle de classification entraîné précédemment."

### Étape 2 : Recherche de Produits (Le point fort)
*   **Action :** Tapez "Je veux voir les robes d'été"
*   **Ce qu'il faut dire :** "Ici, le chatbot identifie l'intention `recherche_produit`. Il extrait les mots-clés et interroge dynamiquement notre base de données MongoDB qui contient maintenant 1000 produits."
*   **Montrez l'affichage :** "Les résultats sont affichés sous forme de cartes avec prix et description."

### Étape 3 : Question sur le service (FAQ)
*   **Action :** Tapez "Comment se passe le retour d'un colis ?"
*   **Ce qu'il faut dire :** "Pour les questions sur les services, le moteur de réponse utilise une collection FAQ spécifique dans MongoDB pour fournir une réponse précise et immédiate."

### Étape 4 : Le Dashboard Analytics
*   **Action :** Cliquez sur l'onglet **Dashboard** dans la barre latérale.
*   **Ce qu'il faut dire :** "En tant qu'administrateur, nous avons accès à des analytics. On peut voir la répartition des intentions de nos clients et le score moyen de confiance du modèle. C'est crucial pour monitorer la qualité du support fourni."

---

# ❓ FAQ Technique - Préparez vos réponses

Voici les questions que votre prof risque de vous poser :

**1. Pourquoi avoir choisi la Logistic Regression plutôt que des réseaux de neurones ?**
> *Réponse :* "C'est un excellent compromis entre performance et simplicité. Pour un volume de données textuelles de ce type, c'est très efficace, facile à debug et très rapide à entraîner."

**2. Comment as-tu géré les 1000 produits ?**
> *Réponse :* "J'ai développé un script d'augmentation de données (`augment_products.py`) qui utilise les produits réels comme templates pour générer des variantes cohérentes. Cela permet de tester la scalabilité du système et de la base MongoDB."

**3. Qu'est-ce que le TF-IDF ?**
> *Réponse :* "C'est une méthode de vectorisation qui transforme le texte en nombres. Elle permet de donner plus d'importance aux mots 'significatifs' et moins aux mots très fréquents qui n'apportent pas d'information."

**4. Si l'utilisateur fait une faute d'orthographe, est-ce que ça marche ?**
> *Réponse :* "Grâce à l'utilisation de N-grammes et au prétraitement (stemming), le modèle est robuste face à certaines petites variations, mais l'intégration d'un correcteur d'orthographe ou de modèles de type Transformers (BERT) serait une amélioration future pour gérer les fautes plus graves."
