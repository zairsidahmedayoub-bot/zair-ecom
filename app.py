import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date
from fpdf import FPDF

# --- CONFIGURATION DIRECTE ---
# On utilise ton lien ici pour ne plus avoir besoin de la boîte "Secrets"
URL_SHEET = "https://docs.google.com/spreadsheets/d/1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# Initialisation de la connexion
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.markdown("### mrhba bik 3nd sidou")

# --- PARTIE 1 : CONVERTISSEUR ---
st.header("1. Convertisseur Square")
taux = 240
montant_euro = st.number_input("Montant en Euro (€) :", min_value=0, value=10)
st.metric("Résultat en DZA", f"{montant_euro * taux:.2f} DA")

st.divider()

# --- PARTIE 2 : COMMANDE ---
st.header("2. Passer une Commande")

col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom complet :")
    tel_client = st.text_input("Téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya :", ["Alger", "Oran", "Sétif", "Autre"])
    produit = st.selectbox("Article :", ["Basket Puma", "Adidas Square", "TN Squale"])

prix_articles = {"Basket Puma": 5500, "Adidas Square": 8500, "TN Squale": 12000}
frais_livraison = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

total = prix_articles[produit] + frais_livraison[wilaya]
st.write(f"### Total à payer : {total} DA")

# --- BOUTON D'ENREGISTREMENT ---
if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom_client and tel_client:
        try:
            # 1. Création de la nouvelle ligne
            nouvelle_ligne = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": tel_client,
                "wilaya": wilaya,
                "produit": produit,
                "total": f"{total} DA"
            }])

            # 2. Lecture des données actuelles via le lien direct
            df_actuel = conn.read(spreadsheet=URL_SHEET)
            
            # 3. Fusion et Mise à jour
            df_final = pd.concat([df_actuel, nouvelle_ligne], ignore_index=True)
            conn.update(spreadsheet=URL_SHEET, data=df_final)
            
            st.success(f"✅ Commande de {nom_client} enregistrée avec succès !")
            
            # 4. Petit PDF de confirmation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "BON DE COMMANDE - ZAIR E-COM", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Client: {nom_client}", ln=True)
            pdf.cell(0, 10, f"Produit: {produit}", ln=True)
            pdf.cell(0, 10, f"Total: {total} DA", ln=True)
            
            pdf_name = f"commande_{nom_client}.pdf"
            pdf.output(pdf_name)
            with open(pdf_name, "rb") as f:
                st.download_button("📥 Télécharger le Bon (PDF)", f, file_name=pdf_name)

        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement : {e}")
    else:
        st.warning("⚠️ Remplis le nom et le téléphone avant de valider.")
