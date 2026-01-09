import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- CONFIGURATION DIRECTE ---
# Ton lien Google Sheets est maintenant directement dans le code
URL_SHEET = "https://docs.google.com/spreadsheets/d/1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# Initialisation de la connexion
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.markdown("### Bienvenue chez Sidou")

# --- FORMULAIRE ---
st.header("Passer une Commande")

col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom complet :")
    tel_client = st.text_input("Téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya :", ["Alger", "Oran", "Sétif", "Autre"])
    produit = st.selectbox("Article :", ["Basket Puma", "Adidas Square", "TN Squale"])

# Tarifs
prix_articles = {"Basket Puma": 5500, "Adidas Square": 8500, "TN Squale": 12000}
frais_livraison = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

total = prix_articles[produit] + frais_livraison[wilaya]
st.write(f"### Total à payer : {total} DA")

# --- BOUTON D'ENREGISTREMENT ---
if st.button("🚀 VALIDER ET ENREGISTRER"):
    if nom_client and tel_client:
        try:
            # 1. Préparation de la nouvelle ligne
            nouvelle_ligne = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": tel_client,
                "wilaya": wilaya,
                "produit": produit,
                "total": f"{total} DA"
            }])

            # 2. Lecture et mise à jour via l'URL directe
            # On utilise .read() puis on concatène
            df_actuel = conn.read(spreadsheet=URL_SHEET)
            df_final = pd.concat([df_actuel, nouvelle_ligne], ignore_index=True)
            
            # 3. Envoi vers Google Sheets
            conn.update(spreadsheet=URL_SHEET, data=df_final)
            
            st.success(f"✅ Commande enregistrée pour {nom_client} !")
            st.balloons()

        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
            st.info("Vérifie bien que ton Google Sheets est partagé en mode 'ÉDITEUR' pour 'Tous ceux qui ont le lien'.")
    else:
        st.warning("⚠️ Remplis tous les champs !")
