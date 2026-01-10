@echo off
echo ========================================
echo   Chatbot E-commerce - Demarrage
echo ========================================
echo.

echo [1/3] Verification des dependances...
python -c "import streamlit, nltk, spacy, sklearn, pymongo" 2>nul
if errorlevel 1 (
    echo Installation des dependances...
    pip install -r requirements.txt
)

echo.
echo [2/3] Installation du modele spaCy...
python -m spacy download fr_core_news_sm

echo.
echo [3/3] Demarrage de l'application...
echo.
streamlit run app.py

pause


