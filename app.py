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

st.set_page_config(page_title="ZAIR SQUAR & E-COM")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")

# --- FORMULAIRE ---
nom = st.text_input("Nom complet :")
tel = st.text_input("Téléphone :")
wilaya = st.selectbox("Wilaya :", list(frais_wilaya.keys()))
produit = st.selectbox("Article :", list(CATALOGUE.keys()))
qte = st.number_input("Quantité :", min_value=1, value=1)
total = (CATALOGUE[produit]["prix"] * qte) + frais_wilaya[wilaya]

if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom and tel:
        try:
            # Préparation des données
            df_new = pd.DataFrame({
                "Date": [str(date.today())],
                "nom": [nom],
                "téléphone": [tel],
                "wilaya": [wilaya],
                "produit": [produit],
                "total": [f"{total} DA"]
            })

            # Lecture et mise à jour simplifiée
            data = conn.read()
            data = pd.concat([data, df_new], ignore_index=True)
            conn.update(data=data)
            
            st.success("✅ Commande enregistrée dans Google Sheets !")
            
            # Génération PDF rapide
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, f"Facture pour {nom}", ln=True, align='C')
            pdf.output("facture.pdf")
            with open("facture.pdf", "rb") as f:
                st.download_button("📥 Télécharger PDF", f, file_name="facture.pdf")

        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
    else:
        st.warning("Remplis tous les champs !")
