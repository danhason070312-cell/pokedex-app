import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")

# עיצוב מודרני (CSS)
st.markdown("""
    <style>
    .card { border: 2px solid #00f2ff; border-radius: 15px; padding: 20px; background: #1a1c23; margin-bottom: 10px; }
    .neon-text { color: #00f2ff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎤 AI Pokedex")

# נתוני גרגירים
berries_data = {
    "Oran": {"Img": "oran.png.png", "Effect": "משחזר 10 נקודות חיים (HP)."},
    "Sitrus": {"Img": "sitrus.png.png", "Effect": "משחזר 25% מהחיים המקסימליים."},
    "Lum": {"Img": "lum.png.png", "Effect": "מרפא כל סטטוס."},
    "Cheri": {"Img": "cheri.png.png", "Effect": "מרפא שיתוק."},
    "Chesto": {"Img": "chesto.png.png", "Effect": "מעיר פוקימון שנרדם."}
}

regions = {"Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386)}

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()
menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    user_input = st.text_input('חפש פוקימון:')
    if user_input:
        match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.3)
        name = match[0] if match else user_input.lower().strip()
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        
        if res.status_code == 200:
            data = res.json()
            species_data = requests.get(data['species']['url']).json()
            desc = next((e['flavor_text'] for e in species_data['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            
            # הקראה אוטומטית
            tts = gTTS(text=desc, lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
            
            st.markdown(f"""
            <div class="card">
                <h2 class="neon-text">{data['name'].upper()}</h2>
                <p><b>Description:</b> {desc}</p>
                <p><i>(תיאור: {desc})</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # צורות ושייני
            varieties = species_data.get('varieties', [])
            for v in varieties:
                v_res = requests.get(v['pokemon']['url']).json()
                img = v_res['sprites']['other']['official-artwork'].get('front_default')
                shiny = v_res['sprites']['other']['official-artwork'].get('front_shiny')
                c1, c2 = st.columns(2)
                if img: c1.image(img, caption=f"{v['pokemon']['name']} (Normal)")
                if shiny: c2.image(shiny, caption=f"{v['pokemon']['name']} (Shiny)")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    for name, d in berries_data.items():
        st.subheader(name)
        st.write(d["Effect"])
