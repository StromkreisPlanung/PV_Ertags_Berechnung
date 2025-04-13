import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="PV-Ertragsauswertung", layout="centered")
st.title("🔋 PV-Ertragsauswertung")
st.markdown("Berechne den Erlös deiner PV-Anlage bei verschiedenen Verkaufspreisen und Anteilen.")

jahresertrag = st.number_input("📥 Jahresertrag (kWh)", min_value=0.0, step=100.0, value=10000.0)
st.subheader("💶 Verkaufspreise und Anteile")
anzahl = st.number_input("Anzahl der Preisstufen", min_value=1, max_value=10, value=3, step=1)

preise = []
prozente = []

for i in range(int(anzahl)):
    col1, col2 = st.columns(2)
    with col1:
        preis = st.number_input(f"Verkaufspreis {i+1} (€/kWh)", min_value=0.01, step=0.01, key=f"preis_{i}")
    with col2:
        prozent = st.number_input(f"Anteil {i+1} (%)", min_value=0.0, max_value=100.0, step=1.0, key=f"proz_{i}")
    preise.append(preis)
    prozente.append(prozent)

if st.button("📈 Auswertung starten") and jahresertrag > 0 and sum(prozente) > 0:
    gesamt_prozent = sum(prozente)
    werte = []
    labels = []
    text_rows = []

    for preis, proz in zip(preise, prozente):
        if preis > 0 and proz > 0:
            kwh = jahresertrag * (proz / gesamt_prozent)
            euro = kwh * preis
            werte.append(euro)
            labels.append(f"{proz:.1f}% @ {preis:.2f} €/kWh\n{euro:.2f} €")
            text_rows.append((preis, proz, kwh, euro))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(werte, labels=labels, startangle=140, colors=plt.cm.Blues(np.linspace(0.3, 0.85, len(werte))))
    ax.set_title("Ertragsverteilung", fontsize=14)
    ax.axis("equal")
    st.pyplot(fig)

    st.subheader("📊 Detailtabelle")
    st.markdown("| Verkaufspreis | Anteil (%) | Energie (kWh) | Ertrag (€) |")
    st.markdown("|---------------|-------------|----------------|-------------|")
    for row in text_rows:
        st.markdown(f"| {row[0]:.2f} | {row[1]:.1f} | {row[2]:.1f} | {row[3]:.2f} |")

    st.success(f"💰 **Gesamtertrag:** {sum(werte):.2f} €")
else:
    st.info("Bitte gib Werte ein und klicke auf 'Auswertung starten'.")
