import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image
import qrcode
from io import BytesIO

# --- CONFIGURATION ---
st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# ID de ton Google Sheet
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.markdown("### Bienvenue chez Sidou")

# --- CONNEXION GOOGLE SHEETS ---
@st.cache_resource
def init_connection():
    """Initialise la connexion avec Google Sheets via Service Account"""
    try:
        # Récupération des secrets depuis Streamlit
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Erreur d'authentification : {e}")
        return None

def get_data():
    """Récupère les données du Google Sheet"""
    try:
        client = init_connection()
        if client:
            sheet = client.open_by_key(SHEET_ID).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return pd.DataFrame()

def add_data(nouvelle_commande):
    """Ajoute une nouvelle commande au Google Sheet"""
    try:
        client = init_connection()
        if client:
            sheet = client.open_by_key(SHEET_ID).sheet1
            sheet.append_row(nouvelle_commande)
            return True
        return False
    except Exception as e:
        st.error(f"Erreur d'écriture : {e}")
        return False

# --- FORMULAIRE ---
st.header("Passer une Commande")

col1, col2 = st.columns(2)

with col1:
    nom_client = st.text_input("Nom complet :")
    tel_client = st.text_input("Téléphone :")

with col2:
    wilaya = st.selectbox("Wilaya :", ["Alger", "Oran", "Sétif", "Autre"])
    produit = st.selectbox("Article :", ["Basket Puma", "Adidas Square", "TN Squale"])

# Tarifs
prix_articles = {"Basket Puma": 5500, "Adidas Square": 8500, "TN Squale": 12000}
frais_livraison = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

total = prix_articles[produit] + frais_livraison[wilaya]
st.write(f"### Total à payer : {total} DA")

# --- BOUTON D'ENREGISTREMENT ---
if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom_client and tel_client:
        nouvelle_commande = [
            str(date.today()),
            nom_client,
            tel_client,
            wilaya,
            produit,
            f"{total} DA"
        ]
        
        if add_data(nouvelle_commande):
            st.success(f"✅ Commande enregistrée pour {nom_client} !")
            st.balloons()
        else:
            st.error("❌ Impossible d'enregistrer la commande.")
    else:
        st.warning("⚠️ Remplis tous les champs !")

# --- AFFICHAGE DES COMMANDES ---
st.markdown("---")
st.header("📋 Historique des Commandes")

if st.button("🔄 Actualiser les données"):
    df_commandes = get_data()
    
    if not df_commandes.empty:
        st.dataframe(df_commandes, use_container_width=True)
        st.info(f"📊 Total de {len(df_commandes)} commande(s)")
    else:
        st.warning("Aucune commande enregistrée pour le moment.")
