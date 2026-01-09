import streamlit as st
from fpdf import FPDF
import qrcode
import os
from datetime import date
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuration du catalogue
CATALOGUE = {
    "Basket Puma": {"prix": 5500, "image": "puma.jpg"},
    "Adidas Square": {"prix": 8500, "image": "adidas.jpg"},
    "TN Squale": {"prix": 12000, "image": "tn.jpg"}
}

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# Initialisation de la connexion Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.subheader("mrhba bik 3nd sidou")

# Formulaire client
nom_client = st.text_input("Nom complet du client :")
telephone = st.text_input("Numéro de téléphone :")
wilaya = st.selectbox("Wilaya de livraison :", ["Alger", "Oran", "Sétif", "Autre"])
produit_nom = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))
quantite = st.number_input("Quantité :", min_value=1, value=1)

frais = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
total_final = (CATALOGUE[produit_nom]["prix"] * quantite) + frais[wilaya]

if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom_client and telephone:
        try:
            # 1. Préparation des données
            nouvelle_donnee = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": telephone,
                "wilaya": wilaya,
                "produit": produit_nom,
                "total": f"{total_final} DA"
            }])

            # 2. Lecture et mise à jour (La magie opère ici)
            existing_data = conn.read()
            updated_data = pd.concat([existing_data, nouvelle_donnee], ignore_index=True)
            conn.update(data=updated_data)
            
            st.success(f"✅ Commande enregistrée pour {nom_client} !")
            
            # 3. Génération du PDF (ton code habituel)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 16)
            pdf.cell(190, 10, "FACTURE ZAIR E-COM", ln=True, align='C')
            pdf.output("facture.pdf")
            with open("facture.pdf", "rb") as f:
                st.download_button("📥 Télécharger la Facture", f, file_name=f"Facture_{nom_client}.pdf")

        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
            st.info("Note : Assure-toi que l'accès au Sheets est 'Éditeur' pour tout le monde.")
    else:
        st.warning("Veuillez remplir tous les champs.")
