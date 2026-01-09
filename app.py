import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date
from fpdf import FPDF

# --- CONFIGURATION ---
# On met le lien directement ici pour ne plus dépendre de la boîte "Secrets"
URL_SHEET = "https://docs.google.com/spreadsheets/d/1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

st.set_page_config(page_title="ZAIR E-COM", layout="wide")

# Connexion forcée avec le lien direct
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")

# --- FORMULAIRE ---
nom = st.text_input("Nom complet :")
tel = st.text_input("Téléphone :")
wilaya = st.selectbox("Wilaya :", ["Alger", "Oran", "Sétif", "Autre"])
produit = st.selectbox("Article :", ["Basket Puma", "Adidas Square", "TN Squale"])
total_da = 6300 

if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom and tel:
        try:
            # On force l'utilisation du lien ici aussi
            df_new = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom,
                "téléphone": tel,
                "wilaya": wilaya,
                "produit": produit,
                "total": f"{total_da} DA"
            }])

            # Lecture et mise à jour en utilisant le lien direct
            existing_data = conn.read(spreadsheet=URL_SHEET)
            updated_data = pd.concat([existing_data, df_new], ignore_index=True)
            
            # Tentative de mise à jour directe
            conn.update(spreadsheet=URL_SHEET, data=updated_data)
            
            st.success(f"✅ Commande enregistrée pour {nom} !")
            
        except Exception as e:
            st.error(f"Erreur : {e}")
            st.info("Note : Si l'erreur persiste, vérifie que le partage est bien sur 'Tous les utilisateurs disposant du lien : EDITEUR' sur Google Sheets.")
    else:
        st.warning("Remplis le nom et le tel !")
