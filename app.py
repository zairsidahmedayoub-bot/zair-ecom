import streamlit as st
from fpdf import FPDF
import qrcode
import os
from datetime import date
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION GOOGLE SHEETS ---
# Remplace l'URL ci-dessous par le lien que tu as copié à l'étape 1
URL_SHEET = "TON_LIEN_COPIE_ICI"

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

# --- SECTION COMMANDE ---
st.header("Générateur de Bon de Commande")
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom complet du client :")
    telephone = st.text_input("Numéro de téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya de livraison :", list(frais_wilaya.keys()))
    adresse = st.text_area("Adresse exacte :")

produit_nom = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))
prix_u = CATALOGUE[produit_nom]["prix"]
quantite = st.number_input("Quantité :", min_value=1, value=1)
total_final = (prix_u * quantite) + frais_wilaya[wilaya]

if st.button("🚀 VALIDER ET GÉNÉRER LA FACTURE"):
    if nom_client and telephone:
        try:
            # 1. ENREGISTREMENT DANS GOOGLE SHEETS
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Création de la ligne de données
            nouvelle_ligne = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": telephone,
                "wilaya": wilaya,
                "produit": produit_nom,
                "total": f"{total_final} DA"
            }])
            
            # Lecture des données existantes et ajout
            existing_data = conn.read(spreadsheet=URL_SHEET)
            updated_data = pd.concat([existing_data, nouvelle_ligne], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=updated_data)
            
            st.success("✅ Commande enregistrée dans la base de données !")

            # 2. GÉNÉRATION DU PDF (Ton code habituel)
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
                st.download_button("📥 Télécharger le PDF", f, file_name=f"Facture_{nom_client}.pdf")

        except Exception as e:
            st.error(f"Erreur : {e}")
    else:
        st.warning("Remplis le nom et le téléphone !")
