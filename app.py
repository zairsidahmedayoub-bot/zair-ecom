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
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="ZAIR LUXE E-COM", layout="wide", page_icon="👟")

# ⚠️ Remplace par ton vrai ID de Google Sheet
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"
TIKTOK_URL = "https://www.tiktok.com/@zair.product"
WHATSAPP_NUMBER = "213782473413" # Ton numéro sans le +

# --- 2. DESIGN "SNEAK PEEK" (DARK & NEON) ---
st.markdown("""
    <style>
    /* Fond noir profond */
    .stApp { background-color: #080a0c !important; color: #ffffff; }
    
    /* Header Galaxie */
    .header-box {
        background: linear-gradient(135deg, #000000 0%, #1c1f26 100%);
        padding: 50px;
        border-radius: 30px;
        text-align: center;
        border: 1px solid #00f2ff;
        margin-bottom: 40px;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.15);
    }
    
    /* Cartes Produits style Inspiration */
    .product-card {
        background: #161a21;
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        border: 1px solid #2d323d;
        transition: 0.4s all;
        margin-bottom: 10px;
    }
    .product-card:hover {
        border-color: #00f2ff;
        transform: translateY(-12px);
        box-shadow: 0 15px 35px rgba(0, 242, 255, 0.2);
    }
    
    /* Titres et Prix */
    h1, h2, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .price-tag { color: #00f2ff; font-size: 24px; font-weight: bold; }

    /* Boutons Néon */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff 0%, #0072ff 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: bold;
        height: 55px;
        font-size: 16px;
        letter-spacing: 1px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6);
    }

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #00f2ff !important; border-bottom-color: #00f2ff !important; }
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

# --- 4. INTERFACE ---
st.markdown("""
    <div class="header-box">
        <h1 style="font-size: 45px; letter-spacing: -1px;">ZAIR LUXE <span style="color:#00f2ff">SNEAKERS</span></h1>
        <p style="color: #888; font-size: 18px;">L'excellence du Square à portée de clic.</p>
    </div>
""", unsafe_allow_html=True)

tab_shop, tab_square, tab_admin = st.tabs(["🛍️ SHOPPING", "💱 CHANGE", "📋 ADMIN"])

with tab_shop:
    produits = {
        "Basket Puma": {"prix": 5500, "img": "puma.jpg", "desc": "Design Minimaliste"},
        "Adidas Square": {"prix": 8500, "img": "adidas.jpg", "desc": "Édition Limitée DZA"},
        "TN Squale": {"prix": 12000, "img": "tn.jpg", "desc": "Premium Performance"}
    }
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(produits.items()):
        with cols[i]:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            if os.path.exists(info['img']):
                st.image(info['img'], use_container_width=True)
            else:
                st.markdown("<div style='height:180px; background:#1c1f26; border-radius:15px; display:flex; align-items:center; justify-content:center; color:#444;'>📷 Photo à venir</div>", unsafe_allow_html=True)
            st.markdown(f"### {name}")
            st.markdown(f"<p class='price-tag'>{info['prix']} DA</p>", unsafe_allow_html=True)
            st.caption(info['desc'])
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>🚀 PASSER MA COMMANDE</h2>", unsafe_allow_html=True)
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("👤 Ton Nom Complet")
            tel = st.text_input("📞 Ton Numéro de Téléphone")
        with c2:
            wilaya = st.selectbox("📍 Wilaya de Livraison", ["Alger", "Oran", "Sétif", "Autre"])
            article = st.selectbox("👟 Modèle choisi", list(produits.keys()))
        
        frais = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
        total = produits[article]['prix'] + frais[wilaya]
        
        st.markdown(f"<div style='text-align:center; padding:30px;'><h1>Total : <span style='color:#00f2ff'>{total} DA</span></h1></div>", unsafe_allow_html=True)
        
        if st.button("🌟 VALIDER ET GÉNÉRER LE BON"):
            if nom and tel:
                if add_data([str(date.today()), nom, tel, wilaya, article, f"{total} DA"]):
                    st.success(f"Félicitations {nom}, commande validée !")
                    st.balloons()
                    
                    # Lien WhatsApp automatique
                    msg = f"Salut Zair Luxe ! Je souhaite commander : {article}. \nNom: {nom}\nTel: {tel}\nWilaya: {wilaya}\nTotal: {total} DA"
                    url_wa = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'''<a href="{url_wa}" target="_blank"><button style="width:100%; height:50px; background:#25D366; color:white; border:none; border-radius:50px; font-weight:bold; cursor:pointer;">📲 ENVOYER PAR WHATSAPP</button></a>''', unsafe_allow_html=True)
                else:
                    st.error("Erreur de connexion à la base de données.")
            else:
                st.warning("⚠️ Remplis tes coordonnées pour commander !")

with tab_square:
    st.markdown("### 💱 CONVERTISSEUR SQUARE")
    taux = st.number_input("Taux Square (Marché Noir) :", value=240)
    montant = st.number_input("Montant :", min_value=0)
    if st.button("Calculer"):
        st.info(f"Résultat : {montant * taux} DA / {montant / taux:.2f} €")

with tab_admin:
    st.markdown("### 📋 HISTORIQUE DES COMMANDES")
    if st.button("🔄 ACTUALISER LES VENTES"):
        df = get_data()
        if not df.empty:
            st.dataframe(df)
            st.metric("Total Commandes", len(df))
