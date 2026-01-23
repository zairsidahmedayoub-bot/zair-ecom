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
st.set_page_config(page_title="ZAIR LUXE E-COM", layout="wide", page_icon="👑")

# Rappel : N'oublie pas de supprimer la boîte secrète lors de l'envoi du code !
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"
TIKTOK_URL = "https://www.tiktok.com/@zair.product"

# --- 2. DESIGN CSS "FULL BLACK & GOLD" ---
st.markdown("""
    <style>
    /* Forcer le fond en noir profond */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Header Luxe */
    .header-box {
        background: linear-gradient(145deg, #000000 0%, #1a1a1a 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #D4AF37;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }
    
    /* Titres en Or */
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif;
    }

    /* Cartes produits Dark */
    .product-card {
        border: 1px solid #333333;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        background-color: #1a1a1a;
        transition: 0.4s ease;
    }
    .product-card:hover {
        transform: scale(1.02);
        border-color: #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }
    
    /* Inputs (champs de saisie) */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }

    /* Boutons Or */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #C5A028 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        height: 55px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
    }

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0E1117;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888;
    }
    .stTabs [aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INTERFACE ---
st.markdown("""
    <div class="header-box">
        <h1 style="margin: 0;">👑 ZAIR SQUAR LUXE 👑</h1>
        <p style="color: #D4AF37; font-size: 1.2rem; letter-spacing: 2px;">PREMIUM QUALITY & FAST DELIVERY</p>
    </div>
""", unsafe_allow_html=True)

tab_boutique, tab_change, tab_admin = st.tabs(["🛍️ CATALOGUE", "💱 CHANGE", "📊 ADMIN"])

with tab_boutique:
    produits = {
        "Basket Puma": {"prix": 5500, "img": "puma.jpg", "desc": "L'élégance sportive"},
        "Adidas Square": {"prix": 8500, "img": "adidas.jpg", "desc": "Édition limitée Square"},
        "TN Squale": {"prix": 12000, "img": "tn.jpg", "desc": "Qualité Or Exceptionnelle"}
    }
    
    cols = st.columns(3)
    for i, (name, info) in enumerate(produits.items()):
        with cols[i]:
            st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
            if os.path.exists(info['img']):
                st.image(info['img'], use_container_width=True)
            else:
                st.markdown("<div style='height:150px; background:#333; border-radius:10px; padding:20px;'>📷 Photo Premium en cours</div>", unsafe_allow_html=True)
            st.subheader(name)
            st.markdown(f"<h2 style='color: #D4AF37;'>{info['prix']} DA</h2>", unsafe_allow_html=True)
            st.caption(info['desc'])
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Formulaire de Commande
    st.markdown("### 📥 RÉSERVER VOTRE ARTICLE")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom complet")
            tel = st.text_input("Téléphone")
        with c2:
            wilaya = st.selectbox("Wilaya de livraison", ["Alger", "Oran", "Sétif", "Autre"])
            article = st.selectbox("Modèle souhaité", list(produits.keys()))
        
        frais_v = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
        total = produits[article]['prix'] + frais_v[wilaya]
        
        st.markdown(f"<div style='text-align:center; padding:20px;'><h3>Total à payer : <span style='color:#D4AF37'>{total} DA</span></h3></div>", unsafe_allow_html=True)
        
        if st.button("🌟 CONFIRMER MA COMMANDE"):
            if nom and tel:
                # Code d'ajout Google Sheets ici
                st.success(f"Félicitations {nom}, votre commande est validée !")
                st.balloons()
            else:
                st.error("Veuillez remplir les informations de contact.")

with tab_change:
    st.markdown("### 💱 CONVERTISSEUR SQUARE")
    # ... (Code du convertisseur identique)

with tab_admin:
    st.markdown("### 📋 SUIVI DES VENTES")
    # ... (Code admin identique)
