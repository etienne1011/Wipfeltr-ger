import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Wipfelträger", page_icon="🌲")

st.title("Wipfelträger")
st.write("Dein Wald reagiert in Echtzeit auf Luftqualitätsdaten weltweit.")


# --- Dropdown ---
orte = {"Naturpark Nassau (Deutschland)": [50.31667, 7.8],
        "Tongariro-Nationalpark (Neuseeland)": [-39.2, 175.5833],
        "Amazonas-Becken (Brasilien)": [-2.5, -60.0],
        "Pekinger Grüngürtel (China)": [39.9042, 116.4074],
        "Hermosa Valley Greenbelt (USA)": [33.9002, -118.3964]}

auswahl = st.selectbox("Wähle einen Ort:", list(orte))
lat = orte[auswahl][0]
lon = orte[auswahl][1]


# --- API-Abfrage ---
url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,pm2_5&hourly=european_aqi&past_days=7&forecast_days=1"

antwort = requests.get(url)
data = antwort.json()

aqi_aktuell = data["current"]["european_aqi"]
pm25_aktuell = data["current"]["pm2_5"]


# --- Logik ---
health = max(0, min(100, 100 - aqi_aktuell))

anzahl_baeume = 38
gesunde_baeume = int(anzahl_baeume * (health/100))
kranke_baeume = anzahl_baeume - gesunde_baeume

if health >= 75:
    zustand = "Dem Wald geht es prima!"
    emoji_diagramm = "🌲" * gesunde_baeume + "🍃" * kranke_baeume
elif health >= 50:
    zustand = "Der Wald atmet schwerer!"
    emoji_diagramm = "🌳" * gesunde_baeume + "🍂" * kranke_baeume
else:
    zustand = "Der Wald ist in Gefahr!"
    emoji_diagramm = "🍂" * gesunde_baeume + "🪵" * kranke_baeume


# --- Darstellung aktueller Zustand ---
st.subheader(f"Aktuelle Zustand in: {auswahl}")
st.info(zustand)

st.markdown(f"<div style='font-size: 28px; line-height: 1.6; background-color: #1e2923; padding: 20px; border-radius: 12px; text-align: center;'>{emoji_diagramm}</div>", unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)
col1.metric("Wald-Gesundheit", f"{health} %")
col2.metric("Schadstoff-Index", f"{aqi_aktuell}")
col3.metric("PM2.5", f"{pm25_aktuell} µg/m³")


# --- Darstellung Verlauf der letzten 7 Tage ---
st.subheader("Verlauf der letzten 7 Tage")
st.caption("Je höher die Kurve (höherer AQI-Wert), desto stärker die Schadstoffbeslastung des Waldes.")

verlauf = pd.DataFrame({
    "Zeitpunkt": pd.to_datetime(data["hourly"]["time"]),
    "Schadstoff-Index (AQI)": data["hourly"]["european_aqi"]})

verlauf = verlauf.set_index("Zeitpunkt")
st.line_chart(verlauf, x_label="Zeitpunkt", y_label="Schadstoffbeslastung")


# --- Infos ---
with st.expander("Infos: Plan, Problem, ToDos"):
    st.markdown("""
    * **Plan:** 
        
        Ich habe meine Idee zuerst auf ein Minimum reduziert. Als Datenquelle habe ich die Open-Meteo Air Quality API gewählt, weil sie öffentlich und ohne Probleme zugänglich ist. Dann habe ich die API-Anfrage und Logik in einem Test-Skript ausprobiert und danach die Streamlit-UI gebaut.

    * **Probleme:** 
        1. Der AQI kann über 100 steigen -> negative Prozentwerte
        2. Syntax und Befehle von Paketen waren mir nicht so vertraut

    * **ToDos:** 
      1. **Mehr Umweltfaktoren:** Satellitendaten zu Waldbränden (NASA API)
      2. **Fehler vorbeugen:** Skript absichern, wenn API nicht antwortet oder Werte fehlen
      3. **Freie Ortssuche**""")