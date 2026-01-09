import streamlit as st
from fpdf import FPDF
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- CONFIGURATION ---
CATALOGUE = {
    "Basket Puma": {"prix": 5500},
    "Adidas Square": {"prix": 8500},
    "TN Squale": {"prix": 12000}
}
frais_wilaya = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# Connexion utilisant le lien dans tes Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.subheader("mrhba bik 3nd sidou")

# --- FORMULAIRE ---
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom complet du client :")
    tel = st.text_input("Numéro de téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya de livraison :", list(frais_wilaya.keys()))
    produit = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))

qte = st.number_input("Quantité :", min_value=1, value=1)
total_da = (CATALOGUE[produit]["prix"] * qte) + frais_wilaya[wilaya]

st.write(f"### Total à payer : {total_da} DA")

if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom and tel:
        try:
            # Préparation de la nouvelle ligne avec les noms exacts de ton Sheets
            df_new = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom,
                "téléphone": tel,
                "wilaya": wilaya,
                "produit": produit,
                "total": f"{total_da} DA"
            }])

            # Lecture et mise à jour
            existing_data = conn.read()
            updated_data = pd.concat([existing_data, df_new], ignore_index=True)
            conn.update(data=updated_data)
            
            st.success(f"✅ Commande enregistrée pour {nom} !")
            
            # Génération d'une facture PDF simplifiée
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 16)
            pdf.cell(190, 10, "FACTURE ZAIR E-COM", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Helvetica", '', 12)
            pdf.cell(100, 10, f"Client: {nom}")
            pdf.ln(10)
            pdf.cell(100, 10, f"Produit: {produit} (x{qte})")
            pdf.ln(10)
            pdf.cell(100, 10, f"Total: {total_da} DA")
            pdf.ln(20)
            pdf.cell(190, 10, "mrhba bik 3nd sidou", align='C')
            
            pdf_file = "facture.pdf"
            pdf.output(pdf_file)
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Télécharger la Facture PDF", f, file_name=f"Facture_{nom}.pdf")

        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
            st.info("Vérifie que ton lien dans les Secrets finit par l'ID du document (sans /edit).")
    else:
        st.warning("⚠️ Remplis tous les champs !")
