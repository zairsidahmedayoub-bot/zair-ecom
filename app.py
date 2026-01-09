import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")

# ⚠️ IMPORTANT : Utilise l'ID du Google Sheet, pas l'URL complète
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

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
            # Initialisation de la connexion
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # 1. Lecture des données actuelles (utilise SHEET_ID au lieu de l'URL)
            df_actuel = conn.read(spreadsheet=SHEET_ID, usecols=list(range(6)))
            
            # 2. Préparation de la nouvelle ligne
            nouvelle_ligne = pd.DataFrame([{
                "Date": str(date.today()),
                "nom": nom_client,
                "téléphone": tel_client,
                "wilaya": wilaya,
                "produit": produit,
                "total": f"{total} DA"
            }])
            
            # 3. Concaténation
            df_final = pd.concat([df_actuel, nouvelle_ligne], ignore_index=True)
            
            # 4. Envoi vers Google Sheets
            conn.update(spreadsheet=SHEET_ID, data=df_final)
            
            st.success(f"✅ Commande enregistrée pour {nom_client} !")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Erreur de connexion : {e}")
            st.info("""
            **Vérifications à faire :**
            1. Va sur ton Google Sheet
            2. Clique sur "Partager" (en haut à droite)
            3. Change "Accès limité" en "Tous ceux qui ont le lien"
            4. Sélectionne "Éditeur" dans le menu déroulant
            5. Clique sur "Terminé"
            
            **Structure requise du Google Sheet :**
            - Colonne A : Date
            - Colonne B : nom
            - Colonne C : téléphone
            - Colonne D : wilaya
            - Colonne E : produit
            - Colonne F : total
            """)
    else:
        st.warning("⚠️ Remplis tous les champs !")

# --- AFFICHAGE DES COMMANDES (optionnel) ---
st.markdown("---")
st.header("📋 Historique des Commandes")

if st.button("🔄 Actualiser les données"):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_commandes = conn.read(spreadsheet=SHEET_ID)
        
        if not df_commandes.empty:
            st.dataframe(df_commandes, use_container_width=True)
            st.info(f"📊 Total de {len(df_commandes)} commande(s)")
        else:
            st.warning("Aucune commande enregistrée pour le moment.")
            
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
