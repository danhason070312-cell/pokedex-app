import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- נתוני עזר ---
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

# רשימת גרגירים מלאה
berries_data = {
    "Oran": "oran-berry", "Sitrus": "sitrus-berry", "Lum": "lum-berry",
    "Cheri": "cheri-berry", "Chesto": "chesto-berry", "Pecha": "pecha-berry",
    "Rawst": "rawst-berry", "Aspear": "aspear-berry", "Persim": "persim-berry"
}

# --- ניווט ---
menu = st.sidebar.radio("בחר קטגוריה:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון:')

    if user_input:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower().strip()}")
        if res.status_code == 200:
            data = res.json()
            species = requests.get(data['species']['url']).json()
            desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(data['sprites']['other']['official-artwork'].get('front_default'), width=300)
            with c2:
                st.subheader(data['name'].upper())
                st.write(f"**מידע:** {desc}")
                # אודיו מקריא את המידע
                tts = gTTS(text=f"{data['name']}. {desc}", lang='en')
                tts.save("p.mp3")
                st.audio("p.mp3", autoplay=True)
    else:
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                st.markdown(f"**#{i}**")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    cols = st.columns(3)
    for i, (name, img_name) in enumerate(berries_data.items()):
        with cols[i % 3]:
            # תמונה מ-PokeAPI
            st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/items/{img_name}.png", width=120)
            st.subheader(f"{name} Berry")
