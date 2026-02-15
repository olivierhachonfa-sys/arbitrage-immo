import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Arbitrage Immo vs Finance", layout="wide")

st.title("🛡️ Simulateur d'Arbitrage Patrimonial")
st.markdown("---")

# --- BARRE LATÉRALE : LES PARAMÈTRES (INPUTS) ---
with st.sidebar:
    st.header("💰 Capital & Fiscalité")
    apport = st.number_input("Apport initial (€)", value=30000, step=5000)
    tmi = st.selectbox("Votre Tranche d'Imposition (TMI %)", [0, 11, 30, 41, 45], index=2) / 100
    duree = st.slider("Durée d'analyse (années)", 5, 25, 20)

    st.header("🏠 Immobilier")
    prix_bien = st.number_input("Prix d'achat du bien (€)", value=180000)
    loyer_hc = st.number_input("Loyer mensuel HC (€)", value=850)
    mensualite = st.number_input("Mensualité Crédit (€)", value=900)
    charges_mens = st.number_input("Charges + Taxe Foncière /mois (€)", value=150)
    
    st.subheader("⚠️ Stress Test Immo")
    vacance = st.slider("Vacance locative (mois par an)", 0, 4, 1)

    st.header("📈 Finance (Bourse)")
    rendement_bourse = st.slider("Rendement annuel espéré (%)", 0.0, 12.0, 7.0) / 100
    
    st.subheader("⚠️ Stress Test Finance")
    krach = st.checkbox("Simuler un Krach (-20%) en année 5")

# --- MOTEUR DE CALCUL ---

# 1. Calcul de l'effort d'épargne (Le "vrai" coût mensuel pour le client)
# On prend en compte la vacance locative dès le départ
loyer_annuel_net = loyer_hc * (12 - vacance)
depenses_annuelles = (mensualite + charges_mens) * 12
effort_annuel = depenses_annuelles - loyer_annuel_net
effort_mensuel = max(0, effort_annuel / 12)

# 2. Simulation année par année
data = []
cap_fin = apport
val_bien = prix_bien
dette = prix_bien - apport

for an in range(1, duree + 1):
    # --- CALCUL FINANCE ---
    r = rendement_bourse
    if krach and an == 5:
        r = -0.20 # Impact du Krach boursier
    
    # On investit l'apport + l'équivalent de l'effort d'épargne immo chaque année
    cap_fin = cap_fin * (1 + r) + (effort_mensuel * 12)
    
    # Fiscalité Finance : Flat Tax 30% sur les plus-values uniquement
    plus_value = cap_fin - (apport + effort_mensuel * 12 * an)
    val_fin_nette = cap_fin - (max(0, plus_value) * 0.30)

    # --- CALCUL IMMOBILIER ---
    val_bien = val_bien * 1.01 # Prise de valeur du bien (+1%/an)
    dette = dette * 0.95 # Remboursement du capital (simplifié à 5%/an)
    val_immo_nette = val_bien - dette

    data.append({
        "Année": an, 
        "Bourse (Net)": round(val_fin_nette), 
        "Immobilier (Net)": round(val_immo_nette)
    })

df = pd.DataFrame(data)

# --- AFFICHAGE DES RÉSULTATS ---

# Métriques clés en haut
c1, c2, c3 = st.columns(3)
c1.metric("Effort d'épargne mensuel", f"{round(effort_mensuel)} €")
c2.metric("Patrimoine Immo à terme", f"{df['Immobilier (Net)'].iloc[-1]:,} €")
c3.metric("Patrimoine Bourse à terme", f"{df['Bourse (Net)'].iloc[-1]:,} €")

# Graphique de comparaison
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Année'], y=df['Immobilier (Net)'], 
    name="Immobilier (Net de dette)", 
    line=dict(color='#1f77b4', width=4)
))
fig.add_trace(go.Scatter(
    x=df['Année'], y=df['Bourse (Net)'], 
    name="Bourse (Net de Flat Tax)", 
    line=dict(color='#2ca02c', width=4)
))

fig.update_layout(
    title="Comparaison de la Richesse Nette sur 20 ans",
    xaxis_title="Années",
    yaxis_title="Valeur Nette (€)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Note informative
st.info(f"💡 Ce simulateur compare l'immobilier avec un placement financier ayant un **effort d'épargne strictement identique** ({round(effort_mensuel)}€/mois). La vacance locative de {vacance} mois réduit mécaniquement la rentabilité de l'immobilier au profit de la bourse.")
