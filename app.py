import streamlit as st

st.set_page_config(page_title="Expert Patrimonial", layout="wide")

st.title("🏦 Audit de votre Patrimoine Actuel")
st.markdown("---")

st.write("Bienvenue. Veuillez renseigner vos actifs ci-dessous pour générer vos projections.")

col1, col2 = st.columns(2)

with col1:
    st.header("💰 Actifs Financiers")
    # On stocke dans session_state pour que les autres pages y accèdent
    st.session_state['cash'] = st.number_input("Liquidités / Livrets (€)", value=10000, step=1000)
    st.session_state['bourse'] = st.number_input("Portefeuille Actions / ETF (€)", value=25000, step=1000)
    st.session_state['epargne_mensuelle'] = st.number_input("Capacité d'épargne mensuelle (€)", value=500, step=100)

with col2:
    st.header("🏠 Actifs Immobiliers")
    st.session_state['immo_val'] = st.number_input("Valeur estimée du parc locatif (€)", value=200000, step=5000)
    st.session_state['immo_dette'] = st.number_input("Capital restant dû (Crédit) (€)", value=120000, step=5000)
    st.session_state['tmi'] = st.selectbox("Votre Tranche d'Imposition (TMI %)", [0, 11, 30, 41, 45], index=2)

st.success("✅ Données enregistrées. Utilisez le menu à gauche pour voir vos projections.")
