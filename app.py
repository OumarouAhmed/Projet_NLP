"""
Application Streamlit principale - Chatbot E-commerce
"""
import os
import sys



import warnings
import streamlit as st
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except Exception:
    # Si sklearn absent ou autre erreur, ne pas bloquer l'application
    pass

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.chatbot_engine import ChatbotEngine
from database.models import ConversationModel, ProductModel
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import config

# Configuration de la page
st.set_page_config(
    page_title="Chatbot E-commerce Mode",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement paresseux (lazy) du chatbot pour éviter des imports lourds au démarrage
@st.cache_resource
def _make_chatbot():
    return ChatbotEngine()

def get_chatbot():
    if "chatbot" not in st.session_state:
        try:
            st.session_state.chatbot = _make_chatbot()
        except Exception as e:
            st.session_state.chatbot = None
            print(f"⚠️ Impossible de créer le chatbot: {e}")
    return st.session_state.chatbot

# Initialisation de la session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot_ready" not in st.session_state:
    st.session_state.chatbot_ready = False

# Sidebar - Navigation
st.sidebar.title("🤖 Chatbot E-commerce")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigation",
    ["💬 Chat", "📊 Dashboard", "📦 Produits", "⚙️ Configuration"]
)

# Page Chat
if page == "💬 Chat":
    st.title("💬 Chatbot de Support Client")
    st.markdown("Posez vos questions sur nos produits, livraisons, paiements, etc.")
    
    # Tentative de chargement du chatbot et du modèle (lazy)
    if not st.session_state.chatbot_ready:
        cb = get_chatbot()
        if cb is None:
            st.error("⚠️ Impossible de créer le chatbot. Vérifiez les logs.")
            st.stop()
        try:
            cb.intent_classifier.load()
            st.session_state.chatbot_ready = True
        except Exception as e:
            st.session_state.chatbot_ready = False
            st.error("⚠️ Le modèle n'a pas été entraîné. Veuillez exécuter le script d'entraînement.")
            st.code("python scripts/train_model.py")
            st.stop()
    
    # Zone de chat (affichée si le modèle est prêt)
    chat_container = st.container()
    
    with chat_container:
        # Afficher l'historique des messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Afficher les produits si disponibles
                if message.get("products"):
                    st.markdown("**Produits suggérés :**")
                    for product in message["products"][:3]:
                        with st.expander(f"🛍️ {product.get('name', 'Produit')} - {product.get('price', 'N/A')}€"):
                            st.write(f"**Catégorie:** {product.get('category', 'N/A')}")
                            st.write(f"**Genre:** {product.get('gender', 'N/A')}")
                            st.write(f"**Description:** {product.get('description', 'N/A')}")
        
        # Zone de saisie
        user_input = st.chat_input("Tapez votre message ici...")
        
        if user_input:
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Obtenir la réponse du chatbot
            with st.spinner("Réflexion en cours..."):
                cb = get_chatbot()
                if cb is None:
                    st.error("⚠️ Chatbot non disponible.")
                    st.stop()
                response = cb.process_message(user_input)

            # Ajouter la réponse du bot
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["response"],
                "intent": response.get("intent"),
                "confidence": response.get("confidence"),
                "products": response.get("products", [])
            })
            
            # Recharger pour afficher les nouveaux messages
            st.rerun()
# Page Dashboard
elif page == "📊 Dashboard":
    st.title("📊 Dashboard Analytics")
    
    try:
        conversation_model = ConversationModel()
        stats = conversation_model.get_conversation_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Conversations", stats["total_conversations"])
        
        with col2:
            avg_confidence = sum(c.get("confidence", 0) for c in stats["recent_conversations"]) / len(stats["recent_conversations"]) if stats["recent_conversations"] else 0
            st.metric("Confiance Moyenne", f"{avg_confidence:.1%}")
        
        with col3:
            unique_intents = len(set(s["_id"] for s in stats["intent_distribution"]))
            st.metric("Intentions Uniques", unique_intents)
        
        with col4:
            today_count = sum(1 for c in stats["recent_conversations"] 
                            if c.get("timestamp") and 
                            isinstance(c["timestamp"], datetime) and
                            c["timestamp"].date() == datetime.now().date())
            st.metric("Aujourd'hui", today_count)
        
        st.markdown("---")
        
        # Graphique de distribution des intentions
        if stats["intent_distribution"]:
            st.subheader("📈 Distribution des Intentions")
            df_intents = pd.DataFrame(stats["intent_distribution"])
            df_intents.columns = ["Intention", "Nombre"]
            
            fig = px.pie(
                df_intents, 
                values="Nombre", 
                names="Intention",
                title="Répartition des intentions"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau des conversations récentes
        st.subheader("💬 Conversations Récentes")
        if stats["recent_conversations"]:
            recent_df = pd.DataFrame([
                {
                    "Message": c["user_message"][:50] + "..." if len(c.get("user_message", "")) > 50 else c.get("user_message", ""),
                    "Intention": c.get("intent", "N/A"),
                    "Confiance": f"{c.get('confidence', 0):.1%}",
                    "Date": c.get("timestamp", "N/A")
                }
                for c in stats["recent_conversations"]
            ])
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune conversation enregistrée")
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des statistiques: {e}")

# Page Produits
elif page == "📦 Produits":
    st.title("📦 Gestion des Produits")
    
    product_model = ProductModel()
    
    # Recherche de produits
    st.subheader("🔍 Recherche de Produits")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("Recherche", "")
    with col2:
        category_filter = st.selectbox("Catégorie", ["Toutes", "robe", "chemise", "pantalon", "t-shirt", "veste", "jupe", "pull", "manteau"])
    with col3:
        gender_filter = st.selectbox("Genre", ["Tous", "homme", "femme", "unisexe"])
    
    if st.button("Rechercher"):
        category = None if category_filter == "Toutes" else category_filter
        gender = None if gender_filter == "Tous" else gender_filter
        query = search_query if search_query else None
        
        products = product_model.search_products(query, category, gender)
        
        if products:
            st.success(f"✅ {len(products)} produit(s) trouvé(s)")
            
            # Afficher les produits
            for product in products:
                with st.expander(f"🛍️ {product.get('name', 'Produit')} - {product.get('price', 'N/A')}€"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Catégorie:** {product.get('category', 'N/A')}")
                        st.write(f"**Genre:** {product.get('gender', 'N/A')}")
                        st.write(f"**Prix:** {product.get('price', 'N/A')}€")
                    with col2:
                        st.write(f"**Tailles:** {', '.join(product.get('size', []))}")
                        st.write(f"**Couleurs:** {', '.join(product.get('color', []))}")
                    st.write(f"**Description:** {product.get('description', 'N/A')}")
        else:
            st.warning("Aucun produit trouvé")
    
    # Liste de tous les produits
    st.markdown("---")
    st.subheader("📋 Tous les Produits")
    
    all_products = product_model.get_all_products()
    if all_products:
        st.info(f"Total: {len(all_products)} produits")
        
        products_df = pd.DataFrame([
            {
                "Nom": p.get("name", "N/A"),
                "Catégorie": p.get("category", "N/A"),
                "Genre": p.get("gender", "N/A"),
                "Prix": f"{p.get('price', 0)}€"
            }
            for p in all_products
        ])
        st.dataframe(products_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Aucun produit dans la base de données")

# Page Configuration
elif page == "⚙️ Configuration":
    st.title("⚙️ Configuration")
    
    st.subheader("🔧 Actions Système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Entraînement du Modèle")
        st.markdown("""
        Pour entraîner le modèle de classification d'intentions :
        ```bash
        python scripts/train_model.py
        ```
        """)
        
        if st.button("🔄 Réentraîner le Modèle"):
            st.info("Exécutez le script d'entraînement dans le terminal")
    
    with col2:
        st.markdown("### Initialisation Base de Données")
        st.markdown("""
        Pour initialiser MongoDB avec les données :
        ```bash
        python scripts/init_database.py
        ```
        """)
        
        if st.button("🔄 Réinitialiser la Base"):
            st.info("Exécutez le script d'initialisation dans le terminal")
    
    st.markdown("---")
    
    st.subheader("📋 Informations Système")
    
    try:
        cb = get_chatbot()
        if cb and hasattr(cb.intent_classifier, 'vectorizer') and cb.intent_classifier.is_trained:
            features_count = len(cb.intent_classifier.vectorizer.get_feature_names_out())
        else:
            features_count = 0
    except:
        features_count = 0
    
    st.markdown(f"""
    - **Modèle NLP:** Classification d'intentions avec TF-IDF + Logistic Regression
    - **Base de données:** MongoDB
    - **Interface:** Streamlit
    - **Intentions supportées:** {features_count} features
    """)
    
    # État du système
    st.markdown("### 🔍 État du Système")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.chatbot_ready:
            st.success("✅ Modèle chargé")
        else:
            st.error("❌ Modèle non chargé")
    
    with col2:
        try:
            from database.mongodb_connection import mongodb
            if mongodb.is_connected():
                st.success(f"✅ MongoDB connecté ({config.DATABASE_NAME})")
            else:
                st.error("❌ MongoDB non connecté")
        except Exception as e:
            st.error(f"❌ MongoDB non connecté: {str(e)[:50]}")
    
    with col3:
        try:
            product_model = ProductModel()
            count = product_model.get_collection().count_documents({})
            st.success(f"✅ {count} produits")
        except:
            st.error("❌ Produits non disponibles")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Chatbot E-commerce Mode**")
st.sidebar.markdown("Version 1.0")

