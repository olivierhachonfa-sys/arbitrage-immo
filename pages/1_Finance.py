import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("📈 Projection de vos Actifs Financiers")

# Récupération des données de la page d'accueil
capital_initial = st.session_state.get('bourse', 25000) + st.session_state.get('cash', 10000)
effort = st.session_state.get('epargne_mensuelle', 500)

st.sidebar.header("Paramètres Marché")
ticker = st.sidebar.selectbox("Indice de référence", ["IWDA.AS", "^GSPC", "^FCHI"], format_func=lambda x: "MSCI World" if "IWDA" in x else "S&P 500" if "GSPC" in x else "CAC 40")

# Récupération automatique du rendement historique sur 10 ans
data = yf.Ticker(ticker).history(period="10y")
rendement_hist = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) ** (1/10) - 1) * 100

st.metric(f"Rendement Historique moyen (10 ans)", f"{rendement_hist:.2f} % / an")

horizon = st.slider("Horizon de projection (années)", 5, 40, 20)
rendement_choisi = st.slider("Hypothèse de rendement futur (%)", 0.0, 12.0, float(rendement_hist))

# Calcul de la courbe
projection = []
cap = capital_initial
for an in range(horizon + 1):
    projection.append({"Année": an, "Capital": round(cap)})
    cap = cap * (1 + rendement_choisi/100) + (effort * 12)

df = px.pd.DataFrame(projection)
fig = px.area(df, x="Année", y="Capital", title="Évolution estimée du capital financier (Net de frais)")
st.plotly_chart(fig, use_container_width=True)
