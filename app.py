import streamlit as st
from fpdf import FPDF
import qrcode
import os
from datetime import date

# --- 1. CONFIGURATION DU CATALOGUE ---
# Ajoute tes produits ici. Assure-toi que les noms d'images existent dans ton dossier.
CATALOGUE = {
    "Basket Puma": {"prix": 5500, "image": "puma.jpg"},
    "Adidas Square": {"prix": 8500, "image": "adidas.jpg"},
    "TN Squale": {"prix": 12000, "image": "tn.jpg"}
}

# Configuration générale
st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide")
LIEN_TIKTOK = "https://www.tiktok.com/@zair.product?_r=1&_t=ZS-92t8mhY25UC"
NUMERO_MAGASIN = "0782473413"
frais_wilaya = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")

# --- SECTION 1 : CONVERTISSEUR SQUARE ---
st.header("1. Convertisseur de Devises")
taux_square = 240 
option_conv = st.selectbox('Sens de conversion :', ('DZA vers Euro (€)', 'Euro (€) vers DZA'))

if option_conv == 'DZA vers Euro (€)':
    montant = st.number_input("Montant en DZA :", min_value=0, value=1000)
    st.metric("Résultat", f"{montant / taux_square:.2f} €")
else:
    montant = st.number_input("Montant en Euros (€) :", min_value=0, value=10)
    st.metric("Résultat", f"{montant * taux_square:.2f} DA")

st.divider()

# --- SECTION 2 : GÉNÉRATEUR DE COMMANDE AUTOMATISÉ ---
st.header("2. Générateur de Bon de Commande")

# Infos Client
col1, col2 = st.columns(2)
with col1:
    nom_client = st.text_input("Nom complet du client :")
    telephone = st.text_input("Numéro de téléphone :")
with col2:
    wilaya = st.selectbox("Wilaya de livraison :", list(frais_wilaya.keys()))
    adresse = st.text_area("Adresse exacte :")

st.subheader("🛍️ Sélection du Produit")
c_img, c_info = st.columns([1, 2])

with c_info:
    # Sélection dynamique depuis le catalogue
    produit_nom = st.selectbox("Choisir l'article :", list(CATALOGUE.keys()))
    
    # Récupération auto des infos
    prix_u = CATALOGUE[produit_nom]["prix"]
    image_path = CATALOGUE[produit_nom]["image"]
    
    quantite = st.number_input("Quantité :", min_value=1, value=1)
    total_final = (prix_u * quantite) + frais_wilaya[wilaya]
    
    st.write(f"### Total à payer : {total_final} DA")
    st.caption(f"Détail : {prix_u} DA x {quantite} + {frais_wilaya[wilaya]} DA (Livraison)")

with c_img:
    # L'image change selon le choix
    if os.path.exists(image_path):
        st.image(image_path, width=250, caption=f"Modèle {produit_nom}")
    else:
        st.error(f"⚠️ Image '{image_path}' non trouvée")

# --- GÉNÉRATION DU PDF ---
if st.button("🚀 GÉNÉRER LA FACTURE PRO"):
    if nom_client and telephone:
        # Créer le QR Code TikTok
        qr = qrcode.make(LIEN_TIKTOK)
        qr.save("qr_code.png")

        pdf = FPDF()
        pdf.add_page()
        
        # En-tête Noir
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 24)
        pdf.cell(190, 25, "ZAIR SQUAR E-COM", ln=True, align='C')

        # Photos et QR Code
        pdf.ln(20)
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=50, w=45)
        
        pdf.image("qr_code.png", x=155, y=50, w=40)
        pdf.set_xy(155, 90)
        pdf.set_font("Arial", 'B', )
