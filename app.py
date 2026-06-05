import streamlit as st
from gtts import gTTS
import requests

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני מחוזות
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

# ניווט באמצעות טאבים
tab1, tab2 = st.tabs(["פוקדקס", "מדריך גרגירים"])

with tab1:
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון:')

    if user_input:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower().strip()}")
        if res.status_code == 200:
            data = res.json()
            
            # הצגת פוקימון שנמצא
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            with col2:
                st.subheader(data['name'].upper())
                st.write(f"**גובה:** {data['height']/10} מטרים")
                if data['sprites']['front_shiny']:
                    st.image(data['sprites']['front_shiny'], width=100, caption="Shiny Form")
            
            # אודיו
            tts = gTTS(text=f"Pokemon {data['name']}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
    else:
        # גלריה מלאה של המחוז שנבחר
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                # הצגת תמונה מ-PokeAPI
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                st.markdown(f"**#{i}**")

with tab2:
    st.subheader("🍎 מדריך גרגירים")
    # ניתן להוסיף כאן את המילון של הגרגירים שלך בחזרה
