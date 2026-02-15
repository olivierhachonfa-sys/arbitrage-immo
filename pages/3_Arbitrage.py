import streamlit as st
import plotly.graph_objects as go

st.title("⚖️ Arbitrage et Aide à la Décision")

# On récupère les données
val_immo = st.session_state.get('immo_val', 200000)
dette = st.session_state.get('immo_dette', 120000)
net_vendeur = (val_immo * 0.93) - dette # 7% de frais de vente estimés

st.write(f"Si vous vendez votre bien aujourd'hui, vous récupérez **{round(net_vendeur)} €** après remboursement de la banque et frais d'agence.")

st.subheader("Simulation : Vendre pour placer en Bourse")
rendement_bourse = st.slider("Rendement cible Bourse (%)", 4.0, 10.0, 7.0) / 100

annees = list(range(1, 21))
maintien_immo = [val_immo - (dette * 0.95**a) for a in annees] # Simplification dette
arbitrage_bourse = [net_vendeur * (1 + rendement_bourse)**a for a in annees]

fig = go.Figure()
fig.add_trace(go.Scatter(x=annees, y=maintien_immo, name="Garder l'Immobilier", line=dict(color='blue', width=3)))
fig.add_trace(go.Scatter(x=annees, y=arbitrage_bourse, name="Vendre et Placer", line=dict(color='green', width=3)))

st.plotly_chart(fig, use_container_width=True)
