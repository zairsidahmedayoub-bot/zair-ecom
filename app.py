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
                st.markdown("<div
