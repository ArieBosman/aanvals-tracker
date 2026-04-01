import streamlit as st
import requests
from datetime import datetime

# --- INSTELLINGEN ---
# De 'formResponse' URL (afgeleid van jouw link)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc8XSAJiu-u17fMA_l7bj91J9cKlb1F-YveiaZ5BlSa6Pd6Vw/formResponse"

# Jouw unieke entry ID's uit de link
ENTRY_IDS = {
    "datum": "entry.227564301",
    "tijd": "entry.713848869",
    "intensiteit": "entry.388099334",
    "spray": "entry.1792744025",
    "duur": "entry.1766217188",
    "beschrijving": "entry.1351356123",
    "bijzonderheden": "entry.770054014"
}

CORRECTE_PIN = "1972"  # Pas dit aan naar je eigen pincode

# --- BEVEILIGING ---
if "ingelogd" not in st.session_state:
    st.session_state["ingelogd"] = False

if not st.session_state["ingelogd"]:
    st.title("🔐 Aanvalsregistratie Log-in")
    pincode_invoer = st.text_input("Voer je pincode in:", type="default")
    if st.button("Log in"):
        if pincode_invoer == CORRECTE_PIN:
            st.session_state["ingelogd"] = True
            st.rerun()
        else:
            st.error("Onjuiste pincode.")
    st.stop()

# --- DE APP INTERFACE ---
st.set_page_config(page_title="Aanvalsregistratie", layout="centered")
st.title("📋 Nieuwe Aanval Registreren")

with st.form("registratie_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        datum = st.date_input("Datum", datetime.now())
    with col2:
        tijd = st.time_input("Tijd van aanval", datetime.now())
    
    intensiteit = st.select_slider("Aanvalsintensiteit (1-5)", options=[1, 2, 3, 4, 5], value=3)
    spray = st.radio("Spray genomen?", ["Ja", "Nee"], horizontal=True)
    duur = st.text_input("Duur van de aanval (bijv. 10 min)")
    beschrijving = st.text_area("Korte beschrijving")
    bijzonderheden = st.text_area("Bijzonderheden")

    submit_button = st.form_submit_button("Gegevens Opslaan")

# --- DATA VERZENDEN ---
if submit_button:
    # Maak het pakketje met data klaar
    form_data = {
        ENTRY_IDS["datum"]: datum.strftime("%d-%m-%Y"),
        ENTRY_IDS["tijd"]: tijd.strftime("%H:%M"),
        ENTRY_IDS["intensiteit"]: intensiteit,
        ENTRY_IDS["spray"]: spray,
        ENTRY_IDS["duur"]: duur,
        ENTRY_IDS["beschrijving"]: beschrijving,
        ENTRY_IDS["bijzonderheden"]: bijzonderheden
    }

    try:
        # Verstuur de data naar Google Forms
        response = requests.post(FORM_URL, data=form_data)
        if response.status_code == 200:
            st.success("✅ Gelukt! De gegevens zijn opgeslagen.")
            st.balloons()
        else:
            st.error(f"Fout bij opslaan (Code: {response.status_code})")
    except Exception as e:
        st.error(f"Er ging iets mis: {e}")

# --- LINK NAAR JE SHEET ---
st.divider()
st.info("De gegevens worden direct opgeslagen in je Google Sheet via Google Forms.")
if st.button("Open Google Sheet"):
    st.write("Klik hier: [Link naar je Sheet](https://docs.google.com/spreadsheets/d/19dS2kDb5ZH0m-UoCgunPjkHX6i1SFMKV1vrAr4XE3E0/edit)")

if st.sidebar.button("Uitloggen"):
    st.session_state["ingelogd"] = False
    st.rerun()