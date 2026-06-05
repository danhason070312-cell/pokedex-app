import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני עזר
regions = {"Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386), "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)}
berries = {"Oran Berry": {"Effect": "החזרת HP", "Best For": "כל פוקימון"}, "Sitrus Berry": {"Effect": "ריפוי חזק", "Best For": "פוקימוני הגנה"}}

# ניווט באמצעות טאבים (פתרון לכפתורים)
tab1, tab2 = st.tabs(["פוקדקס", "מדריך גרגירים"])

with tab1:
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון:')
    
    if user_input:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower().strip()}")
        if res.status_code == 200:
            data = res.json()
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(data['name'].upper())
            # אודיו אוטומטי
            tts = gTTS(text=f"Pokemon {data['name']}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
    else:
        st.subheader(f"פוקימוני {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                # הצגת תמונה ושם מתחת
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                st.caption(f"#{i}")

with tab2:
    st.subheader("🍎 מדריך גרגירים")
    berry_name = st.selectbox("בחר גרגיר:", list(berries.keys()))
    st.info(f"השפעה: {berries[berry_name]['Effect']} | מתאים ל: {berries[berry_name]['Best For']}")
