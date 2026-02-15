import streamlit as st

st.title("🏠 Analyse Immobilière Net-Net")

val_bien = st.session_state.get('immo_val', 200000)
tmi = st.session_state.get('tmi', 30) / 100

st.subheader("Détails des flux locatifs")
loyer = st.number_input("Loyer mensuel HC (€)", value=900)
charges = st.number_input("Charges + Taxe Foncière (€/mois)", value=180)

# Calcul Fiscalité (Micro-foncier par défaut)
revenu_brut = loyer * 12
revenu_imposable = revenu_brut * 0.70 # Abattement de 30%
impot = revenu_imposable * tmi
ps = revenu_imposable * 0.172 # Prélèvements sociaux

net_net = revenu_brut - (charges * 12) - impot - ps

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Revenu Brut Annuel", f"{revenu_brut} €")
c2.metric("Fiscalité Totale", f"-{round(impot + ps)} €")
c3.metric("Cash-flow Net-Net", f"{round(net_net)} €")

st.info(f"Votre rendement net de fiscalité est de **{((net_net / val_bien)*100):.2f}%**.")
