import streamlit as st
import pandas as pd
from datetime import date
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image
import qrcode
from io import BytesIO
from fpdf import FPDF
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="ZAIR SQUAR & E-COM", layout="wide", page_icon="🛍️")

# ID de ton Google Sheet
SHEET_ID = "1bErvQg4-f2Fga6nRJO8aKYdEOjcC6HMzXa2T7zJLeE0"

# Lien TikTok
TIKTOK_URL = "https://www.tiktok.com/@zair.product"

# CSS personnalisé
st.markdown("""
    <style>
    .product-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        background-color: #fafafa;
        transition: transform 0.3s;
    }
    .product-card:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💸 ZAIR SQUAR & 🛒 ZAIR E-COM")
st.markdown("### 🌟 Bienvenue chez Sidou - Vos articles préférés !")

# --- CONNEXION GOOGLE SHEETS ---
@st.cache_resource
def init_connection():
    """Initialise la connexion avec Google Sheets via Service Account"""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Erreur d'authentification : {e}")
        return None

def get_data():
    """Récupère les données du Google Sheet"""
    try:
        client = init_connection()
        if client:
            sheet = client.open_by_key(SHEET_ID).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
        return pd.DataFrame()

def add_data(nouvelle_commande):
    """Ajoute une nouvelle commande au Google Sheet"""
    try:
        client = init_connection()
        if client:
            sheet = client.open_by_key(SHEET_ID).sheet1
            sheet.append_row(nouvelle_commande)
            return True
        return False
    except Exception as e:
        st.error(f"Erreur d'écriture : {e}")
        return False

def generate_qr_code(url):
    """Génère un QR code pour le lien TikTok"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def create_invoice_pdf(nom, tel, wilaya, produit, total, num_commande):
    """Crée une facture PDF avec QR code"""
    pdf = FPDF()
    pdf.add_page()
    
    # En-tête
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "ZAIR SQUAR & E-COM", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Bienvenue chez Sidou", ln=True, align="C")
    pdf.ln(10)
    
    # Titre Facture
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"FACTURE N° {num_commande}", ln=True, align="C")
    pdf.ln(5)
    
    # Date
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Date: {date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)
    
    # Informations client
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "INFORMATIONS CLIENT", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Nom: {nom}", ln=True)
    pdf.cell(0, 8, f"Telephone: {tel}", ln=True)
    pdf.cell(0, 8, f"Wilaya: {wilaya}", ln=True)
    pdf.ln(10)
    
    # Détails commande
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "DETAILS DE LA COMMANDE", ln=True)
    pdf.ln(2)
    
    # Tableau
    pdf.set_font("Arial", "B", 11)
    pdf.cell(100, 10, "Article", border=1)
    pdf.cell(40, 10, "Prix", border=1, align="C")
    pdf.cell(40, 10, "Livraison", border=1, align="C", ln=True)
    
    # Prix articles
    prix_articles = {
        "Basket Puma": 5500, 
        "Adidas Square": 8500, 
        "TN Squale": 12000,
        "La Fleur de la Nuit": 3500
    }
    frais_livraison = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
    
    prix_produit = prix_articles[produit]
    frais = frais_livraison[wilaya]
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(100, 10, produit, border=1)
    pdf.cell(40, 10, f"{prix_produit} DA", border=1, align="C")
    pdf.cell(40, 10, f"{frais} DA", border=1, align="C", ln=True)
    
    # Total
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(140, 10, "TOTAL A PAYER:", align="R")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, f"{total} DA", align="C")
    pdf.ln(20)
    
    # QR Code
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Suivez-nous sur TikTok:", ln=True, align="C")
    
    # Générer QR code et le sauvegarder temporairement
    qr_img = generate_qr_code(TIKTOK_URL)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    
    # Sauvegarder temporairement pour FPDF
    with open("/tmp/qr_temp.png", "wb") as f:
        f.write(qr_buffer.getvalue())
    
    # Ajouter QR au PDF (centré)
    pdf.image("/tmp/qr_temp.png", x=75, y=pdf.get_y(), w=60)
    pdf.ln(65)
    
    # Pied de page
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Merci pour votre confiance!", ln=True, align="C")
    pdf.cell(0, 8, "ZAIR SQUAR & E-COM - Contact: +213 XXX XXX XXX", ln=True, align="C")
    
    return pdf.output(dest="S").encode("latin1")

# --- CATALOGUE PRODUITS ---
st.header("🛍️ Nos Produits")

# Définition des produits avec leurs infos
produits_catalogue = {
    "Basket Puma": {
        "prix": 5500,
        "image": "puma.jpg",
        "description": "Basket Puma confortable et stylé",
        "emoji": "👟"
    },
    "Adidas Square": {
        "prix": 8500,
        "image": "adidas.jpg",
        "description": "Adidas Square - Design moderne",
        "emoji": "👟"
    },
    "TN Squale": {
        "prix": 12000,
        "image": "tn.jpg",
        "description": "TN Squale - Qualité premium",
        "emoji": "👟"
    },
    "La Fleur de la Nuit": {
        "prix": 3500,
        "image": "fleur.jfif",
        "description": "Parfum La Fleur de la Nuit",
        "emoji": "🌸"
    }
}

# Affichage en grille
cols = st.columns(4)

for idx, (nom_produit, infos) in enumerate(produits_catalogue.items()):
    with cols[idx]:
        st.markdown(f"### {infos['emoji']} {nom_produit}")
        
        # Essayer d'afficher l'image si elle existe
        try:
            if os.path.exists(infos['image']):
                img = Image.open(infos['image'])
                st.image(img, use_container_width=True)
            else:
                # Image placeholder si le fichier n'existe pas
                st.info(f"📷 Photo à venir")
        except:
            st.info(f"📷 Photo à venir")
        
        st.markdown(f"**{infos['description']}**")
        st.markdown(f"### 💰 {infos['prix']} DA")

st.markdown("---")

# --- FORMULAIRE ---
st.header("📝 Passer une Commande")

col1, col2 = st.columns(2)

with col1:
    nom_client = st.text_input("👤 Nom complet :")
    tel_client = st.text_input("📱 Téléphone :")

with col2:
    wilaya = st.selectbox("📍 Wilaya :", ["Alger", "Oran", "Sétif", "Autre"])
    produit_selectionne = st.selectbox(
        "🛒 Choisissez votre article :", 
        list(produits_catalogue.keys())
    )

# Afficher l'image du produit sélectionné
st.markdown("### 🎯 Article sélectionné :")
col_img, col_info = st.columns([1, 2])

with col_img:
    try:
        if os.path.exists(produits_catalogue[produit_selectionne]['image']):
            img = Image.open(produits_catalogue[produit_selectionne]['image'])
            st.image(img, width=200)
        else:
            st.info("📷 Photo à venir")
    except:
        st.info("📷 Photo à venir")

with col_info:
    st.markdown(f"**Produit :** {produit_selectionne}")
    st.markdown(f"**Prix :** {produits_catalogue[produit_selectionne]['prix']} DA")
    
    # Tarifs
    frais_livraison = {"Alger": 500, "Oran": 800, "Sétif": 600, "Autre": 1000}
    frais = frais_livraison[wilaya]
    
    st.markdown(f"**Frais de livraison ({wilaya}) :** {frais} DA")
    
    total = produits_catalogue[produit_selectionne]['prix'] + frais
    st.markdown(f"### 💳 **Total à payer : {total} DA**")

# --- BOUTON D'ENREGISTREMENT ---
st.markdown("---")
if st.button("🚀 VALIDER ET ENREGISTRER LA COMMANDE", use_container_width=True):
    if nom_client and tel_client:
        # Générer numéro de commande unique
        df_existant = get_data()
        num_commande = len(df_existant) + 1 if not df_existant.empty else 1
        
        nouvelle_commande = [
            str(date.today()),
            nom_client,
            tel_client,
            wilaya,
            produit_selectionne,
            f"{total} DA"
        ]
        
        if add_data(nouvelle_commande):
            st.success(f"✅ Commande #{num_commande} enregistrée pour {nom_client} !")
            st.balloons()
            
            # Stocker les infos dans session_state pour télécharger la facture
            st.session_state['derniere_commande'] = {
                'nom': nom_client,
                'tel': tel_client,
                'wilaya': wilaya,
                'produit': produit_selectionne,
                'total': total,
                'num': num_commande
            }
            
            st.info("👇 Téléchargez votre facture ci-dessous")
        else:
            st.error("❌ Impossible d'enregistrer la commande.")
    else:
        st.warning("⚠️ Remplis tous les champs !")

# --- TÉLÉCHARGEMENT FACTURE ---
if 'derniere_commande' in st.session_state:
    st.markdown("---")
    st.subheader("📄 Télécharger votre Facture")
    
    cmd = st.session_state['derniere_commande']
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("📥 TÉLÉCHARGER LA FACTURE PDF", use_container_width=True):
            pdf_data = create_invoice_pdf(
                cmd['nom'], cmd['tel'], cmd['wilaya'], 
                cmd['produit'], cmd['total'], cmd['num']
            )
            
            st.download_button(
                label="💾 Cliquez ici pour télécharger",
                data=pdf_data,
                file_name=f"Facture_ZAIR_{cmd['num']}_{cmd['nom']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# --- AFFICHAGE DES COMMANDES ---
st.markdown("---")
st.header("📋 Historique des Commandes")

if st.button("🔄 Actualiser les données"):
    df_commandes = get_data()
    
    if not df_commandes.empty:
        st.dataframe(df_commandes, use_container_width=True)
        
        # Statistiques
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("📊 Total commandes", len(df_commandes))
        with col_stat2:
            st.metric("🌍 Wilayas servies", df_commandes['wilaya'].nunique())
        with col_stat3:
            produit_populaire = df_commandes['produit'].mode()[0] if not df_commandes.empty else "N/A"
            st.metric("🔥 Produit populaire", produit_populaire)
    else:
        st.warning("Aucune commande enregistrée pour le moment.")
