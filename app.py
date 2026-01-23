import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image
import qrcode
from io import BytesIO
from fpdf import FPDF
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ZAIR LUXE E-COM", layout="wide", page_icon="💎")

# Rappel : N'oublie pas de supprimer la boîte secrète lors de l'envoi du code !
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"
TIKTOK_URL = "https://www.tiktok.com/@zair.product"

# --- 2. DESIGN CSS PERSONNALISÉ (STYLE NOIR ET OR) ---
st.markdown("""
    <style>
    /* Fond général */
    .stApp { background-color: #ffffff; }
    
    /* Header stylé */
    .header-box {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border-bottom: 4px solid #D4AF37;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    /* Cartes produits */
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        background-color: white;
        transition: 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .product-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.1);
        border-color: #D4AF37;
    }
    
    /* Boutons personnalisés */
    .stButton>button {
        background: linear-gradient(90deg, #000000 0%, #333333 100%);
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px;
        font-weight: bold;
        height: 50px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #D4AF37;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIQUE GOOGLE SHEETS ---
@st.cache_resource
def init_connection():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        return gspread.authorize(credentials)
    except: return None

def get_data():
    try:
        client = init_connection()
        if client:
            sheet = client.open_by_key(SHEET_ID).sheet1
            return pd.DataFrame(sheet.get_all_records())
        return pd.DataFrame()
    except: return pd.DataFrame()

def add_data(row):
    try:
        client = init_connection()
        if client:
            client.open_by_key(SHEET_ID).sheet1.append_row(row)
            return True
        return False
    except: return False

# --- 4. INTERFACE PRINCIPALE ---
st.markdown("""
    <div class="header-box">
        <h1 style="color: #D4AF37; margin: 0; font-family: 'Trebuchet MS';">💸 ZAIR SQUAR & E-COM 🛒</h1>
        <p style="color: #ffffff; font-size: 1.2rem; opacity: 0.8;">La qualité Square, livrée chez vous.</p>
    </div>
""", unsafe_allow_html=True)

# ORGANISATION EN ONGLETS
tab_boutique, tab_change, tab_admin = st.tabs(["🛍️ BOUTIQUE", "💱 CHANGE SQUARE", "📋 GESTION"])

with tab_boutique:
    # CATALOGUE
    produits = {
        "Basket Puma": {"prix": 5500, "img": "puma.jpg", "desc": "Confort et style Puma"},
        "Adidas Square": {"prix": 8500, "img": "adidas.jpg", "desc": "Design Square exclusif"},
        "TN Squale": {"prix": 12000, "img": "tn.jpg", "desc": "Qualité Premium TN"}
    }
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(produits.items()):
        with cols[i]:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            if os.path.exists(info['img']):
                st.image(info['img'], use_container_width=True)
            else:
                st.info("📷 Image bientôt disponible")
            st.subheader(name)
            st.markdown(f"**{info['prix']} DA**")
            st.caption(info['desc'])
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # FORMULAIRE
    st.markdown("### 📝 PASSER MA COMMANDE")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("👤 Votre Nom complet")
            tel = st.text_input("📱 Votre Numéro de téléphone")
        with c2:
            wilaya = st.selectbox("📍 Wilaya", ["Alger", "Oran", "Sétif", "Autre"])
            article = st.selectbox("🛒 Article choisi", list(produits.keys()))
        
        frais_v = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
        total = produits[article]['prix'] + frais_v[wilaya]
        
        st.markdown(f"## Total : `{total} DA` (Livraison incluse)")
        
        if st.button("🚀 VALIDER MA COMMANDE"):
            if nom and tel:
                if add_data([str(date.today()), nom, tel, wilaya, article, f"{total} DA"]):
                    st.success("✅ Commande enregistrée ! Téléchargez votre facture ci-dessous.")
                    st.balloons()
                    st.session_state['cmd'] = {'nom': nom, 'tel': tel, 'wilaya': wilaya, 'art': article, 'total': total}
                else: st.error("Erreur de connexion.")
            else: st.warning("Veuillez remplir vos informations.")

    # FACTURE
    if 'cmd' in st.session_state:
        # (Ici tu peux remettre ta fonction PDF existante pour le téléchargement)
        st.info(f"Facture prête pour {st.session_state['cmd']['nom']} !")

with tab_change:
    st.markdown("### 💱 CALCULATEUR MARCHÉ NOIR")
    taux = st.number_input("Taux actuel (Square) :", value=240)
    m_input = st.number_input("Montant à convertir :", min_value=0)
    mode = st.radio("Direction :", ["Euro vers DZA", "DZA vers Euro"])
    
    if mode == "Euro vers DZA":
        st.metric("Résultat", f"{m_input * taux} DA")
    else:
        st.metric("Résultat", f"{m_input / taux:.2f} €")

with tab_admin:
    st.markdown("### 📊 DASHBOARD DES VENTES")
    if st.button("🔄 ACTUALISER LES VENTES"):
        df = get_data()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.metric("Total des ventes", f"{len(df)} commandes")
        else: st.write("Aucune donnée.")
