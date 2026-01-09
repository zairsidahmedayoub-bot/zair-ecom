import streamlit as st
from fpdf import FPDF
import qrcode
import os
from datetime import date
import pandas as pd

# --- CATALOGUE ---
CATALOGUE = {
    "Basket Puma": {"prix": 5500, "image": "puma.jpg"},
    "Adidas Square": {"prix": 8500, "image": "adidas.jpg"},
    "TN Squale": {"prix": 12000, "image": "tn.jpg"}
}

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")
LIEN_TIKTOK = "https://www.tiktok.com/@zair.product?_r=1&_t=ZS-92t8mhY25UC"
NUMERO_MAGASIN = "0782473413"
frais_wilaya = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.subheader("mrhba bik 3nd sidou")

# --- FORMULAIRE ---
nom_client = st.text_input("Nom complet du client :")
telephone = st.text_input("Numéro de téléphone :")
wilaya = st.selectbox("Wilaya de livraison :", list(frais_wilaya.keys()))
produit_nom = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))
quantite = st.number_input("Quantité :", min_value=1, value=1)
total_final = (CATALOGUE[produit_nom]["prix"] * quantite) + frais_wilaya[wilaya]

if st.button("🚀 VALIDER ET GÉNÉRER LA FACTURE"):
    if nom_client and telephone:
        # --- ENREGISTREMENT LOCAL (Pour le test) ---
        # Comme Google bloque l'écriture directe sans clé secrète, 
        # on affiche les données pour confirmer la réception.
        st.toast(f"Commande reçue pour {nom_client} !", icon='✅')
        
        # --- GÉNÉRATION DU PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(190, 10, "FACTURE ZAIR E-COM", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(100, 10, f"Client: {nom_client}")
        pdf.ln(10)
        pdf.cell(100, 10, f"Produit: {produit_nom} (x{quantite})")
        pdf.ln(10)
        pdf.cell(100, 10, f"Total: {total_final} DA")
        pdf.ln(20)
        pdf.cell(190, 10, "mrhba bik 3nd sidou", align='C')
        
        pdf_file = "facture.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Télécharger la Facture PDF", f, file_name=f"Facture_{nom_client}.pdf")
            
        # Affiche un récapitulatif pour toi (le vendeur)
        st.info(f"RÉCAP : {nom_client} | {telephone} | {wilaya} | {total_final} DA")
    else:
        st.warning("Remplis le nom et le téléphone !")
