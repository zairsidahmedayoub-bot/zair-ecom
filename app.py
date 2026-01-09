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

# Connexion Google Sheets
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
            nouvelle_commande = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": telephone,
                "wilaya": wilaya,
                "produit": produit_nom,
                "total": f"{total_final} DA"
            }])

            # Lecture des données existantes
            data_actuelle = conn.read()
            # Fusion
            data_mise_a_jour = pd.concat([data_actuelle, nouvelle_commande], ignore_index=True)
            # Mise à jour du Sheets
            conn.update(data=data_mise_a_jour)
            
            st.success(f"✅ Commande de {nom_client} enregistrée !")

            # B. Génération du PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 16)
            pdf.cell(190, 10, "ZAIR SQUAR E-COM", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Helvetica", '', 12)
            pdf.cell(100, 10, f"Client: {nom_client}")
            pdf.ln(10)
            pdf.cell(100, 10, f"Produit: {produit_nom} (x{quantite})")
            pdf.ln(10)
            pdf.cell(100, 10, f"Total: {total_final} DA")
            pdf.ln(20)
            pdf.set_font("Helvetica", 'B', 14)
            pdf.cell(190, 10, "mrhba bik 3nd sidou", align='C')
            
            pdf_file = "facture.pdf"
            pdf.output(pdf_file)
            
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Télécharger la Facture PDF", f, file_name=f"Facture_{nom_client}.pdf")

        except Exception as e:
            st.error(f"Erreur : {e}")
    else:
        st.warning("⚠️ Remplis le nom et le téléphone !")
