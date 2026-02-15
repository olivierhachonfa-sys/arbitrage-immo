# arbitrage-immo
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Arbitrage Immo vs Finance", layout="wide")

st.title("🛡️ Simulateur d'Arbitrage Patrimonial")
st.markdown("---")

# --- SIDEBAR : LES INPUTS ---
with st.sidebar:
    st.header("💰 Capital & Fiscalité")
    apport = st.number_input("Apport initial (€)", value=30000, step=5000)
    tmi = st.selectbox("Votre TMI (%)", [0, 11, 30, 41, 45], index=2) / 100
    duree = st.slider("Durée d'analyse (ans)", 5, 25, 20)

    st.header("🏠 Immobilier")
    prix_bien = st.number_input("Prix du bien (€)", value=180000)
    loyer_hc = st.number_input("Loyer mensuel HC (€)", value=850)
    charges_mens = st.number_input("Charges + Taxe Foncière /mois (€)", value=150)
    mensualite = st.number_input("Mensualité Crédit (€)", value=900)
    st.subheader("⚠️ Stress Test Immo")
    vacance = st.slider("Vacance locative (mois/an)", 0, 4, 1)

    st.header("📈 Finance")
    rendement_bourse = st.slider("Rendement annuel espéré (%)", 0.0, 12.0, 7.0) / 100
    st.subheader("⚠️ Stress Test Finance")
    krach = st.checkbox("Simuler un Krach (-20%) en année 5")

# --- MOTEUR DE CALCUL ---
loyer_annuel = loyer_hc * (12 - vacance)
sorties_annuelles = (mensualite + charges_mens) * 12
effort_mensuel = max(0, (sorties_annuelles - loyer_annuel) / 12)

data = []
cap_fin = apport
val_bien = prix_bien
dette = prix_bien - apport

for an in range(1, duree + 1):
    # FINANCE
    r = rendement_bourse
    if krach and an == 5: r = -0.20
    cap_fin = cap_fin * (1 + r) + (effort_mensuel * 12)
    # Net de Flat Tax (30%)
    pv = cap_fin - (apport + effort_mensuel * 12 * an)
    val_fin_nette = cap_fin - (max(0, pv) * 0.30)

    # IMMO
    val_bien = val_bien * 1.01 # +1% appreciation
    dette = dette * 0.95 # Amortissement simplifié
    val_immo_nette = val_bien - dette

    data.append({"Année": an, "Bourse": round(val_fin_nette), "Immo": round(val_immo_nette)})

df = pd.DataFrame(data)

# --- AFFICHAGE ---
c1, c2, c3 = st.columns(3)
c1.metric("Effort d'épargne mensuel", f"{round(effort_mensuel)} €")
c2.metric("Patrimoine Immo (Net)", f"{df['Immo'].iloc[-1]:,} €")
c3.metric("Patrimoine Bourse (Net)", f"{df['Bourse'].iloc[-1]:,} €")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Année'], y=df['Immo'], name="Immobilier (Net de dette)", line=dict(color='#1f77b4', width=3)))
fig.add_trace(go.Scatter(x=df['Bourse'], y=df['Bourse'], name="Bourse (Net de Flat Tax)", line=dict(color='#2ca02c', width=3)))
fig.update_layout(hovermode="x unified", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.success(f"Analyse : Pour l'immobilier, nous avons simulé une année à {12-vacance} mois de loyer (risque de vacance pris en compte).")
