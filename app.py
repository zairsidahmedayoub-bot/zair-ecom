import streamlit as st
from fpdf import FPDF
import qrcode
import os
from datetime import date
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. CONFIGURATION ---
CATALOGUE = {
    "Basket Puma": {"prix": 5500, "image": "puma.jpg"},
    "Adidas Square": {"prix": 8500, "image": "adidas.jpg"},
    "TN Squale": {"prix": 12000, "image": "tn.jpg"}
}

frais_wilaya = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
NUMERO_MAGASIN = "0782473413"
LIEN_TIKTOK = "https://www.tiktok.com/@zair.product?_r=1&_t=ZS-92t8mhY25UC"

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# Initialisation de la connexion Google Sheets (utilise les Secrets configurés)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- INTERFACE ---
st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.subheader("mrhba bik 3nd sidou")

# Section 1 : Convertisseur
st.header("1. Convertisseur Square")
taux = 240
option_conv = st.selectbox('Sens :', ('DZA vers Euro (€)', 'Euro (€) vers DZA'))
montant_init = 1000 if option_conv == 'DZA vers Euro (€)' else 10
montant = st.number_input("Montant :", min_value=0, value=montant_init)

if option_conv == 'DZA vers Euro (€)':
    st.metric("Résultat", f"{montant / taux:.2f} €")
else:
    st.metric("Résultat", f"{montant * taux:.2f} DA")

st.divider()

# Section 2 : Commande
st.header("2. Générateur de Bon de Commande")

col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom complet du client :")
    telephone = st.text_input("Numéro de téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya de livraison :", list(frais_wilaya.keys()))
    adresse = st.text_area("Adresse exacte :")

st.subheader("🛍️ Sélection du Produit")
produit_nom = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))
quantite = st.number_input("Quantité :", min_value=1, value=1)

total_final = (CATALOGUE[produit_nom]["prix"] * quantite) + frais_wilaya[wilaya]
st.write(f"### Total à payer : {total_final} DA")

# --- BOUTON FINAL : ENREGISTREMENT ET PDF ---
if st.button("🚀 VALIDER ET ENREGISTRER LA COMMANDE"):
    if nom_client and telephone:
        try:
            # A. Enregistrement Google Sheets
            nouvelle_commande =
