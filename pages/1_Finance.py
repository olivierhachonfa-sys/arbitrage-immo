import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Projection Financière", layout="wide")

st.title("📈 Projection de vos Actifs Financiers")

# 1. Récupération des données de la page d'accueil (ou valeurs par défaut)
capital_bourse = st.session_state.get('bourse', 25000)
capital_cash = st.session_state.get('cash', 10000)
capital_initial = capital_bourse + capital_cash
effort = st.session_state.get('epargne_mensuelle', 500)

# 2. Barre latérale pour les paramètres de marché
st.sidebar.header("⚙️ Paramètres de Simulation")
ticker = st.sidebar.selectbox(
    "Indice de référence", 
    ["IWDA.AS", "^GSPC", "^FCHI"], 
    format_func=lambda x: "MSCI World (Acc)" if "IWDA" in x else "S&P 500 (USA)" if "GSPC" in x else "CAC 40 (France)"
)

# Récupération automatique du rendement historique réel via yfinance
try:
    data = yf.Ticker(ticker).history(period="10y")
    # Calcul du rendement annuel composé (CAGR)
    rendement_hist = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) ** (1/10) - 1) * 100
except Exception:
    rendement_hist = 7.0  # Valeur de secours si l'API échoue

st.metric(f"Rendement Historique moyen (10 ans)", f"{rendement_hist:.2f} % / an")

# 3. Sliders pour ajuster la projection
horizon = st.slider("Horizon de projection (années)", 1, 40, 20)
rendement_choisi = st.slider("Hypothèse de rendement futur (%)", 0.0, 15.0, float(rendement_hist))

# 4. Calcul de la courbe de capitalisation
projection = []
cap = capital_initial
for an in range(horizon + 1):
    projection.append({"Année": an, "Capital": round(cap)})
    cap = cap * (1 + rendement_choisi/100) + (effort * 12)

# 5. Création du graphique avec correction du bug DataFrame
df_proj = pd.DataFrame(projection) # Utilisation correcte de pandas

fig = px.area(
    df_proj, 
    x="Année", 
    y="Capital", 
    title=f"Évolution estimée du capital (Rendement : {rendement_choisi}%)",
    labels={"Capital": "Valeur du portefeuille (€)", "Année": "Nombre d'années"}
)

# Personnalisation esthétique du graphique
fig.update_traces(line_color='#2ca02c', fillcolor='rgba(44, 160, 44, 0.2)')
st.plotly_chart(fig, use_container_width=True)

# 6. Résumé chiffré
final_cap = df_proj['Capital'].iloc[-1]
gain = final_cap - capital_initial - (effort * 12 * horizon)

col1, col2 = st.columns(2)
col1.success(f"**Capital final estimé :** {final_cap:,.0f} €")
col2.info(f"**Total des intérêts générés :** {gain:,.0f} €")
