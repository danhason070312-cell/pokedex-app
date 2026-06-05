import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני עזר
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

berries_data = {
    "Oran Berry": {"Img": "oran-berry", "Loc": "Routes 102, 104", "Effect": "Restores 10 HP", "Best": "General use"},
    "Sitrus Berry": {"Img": "sitrus-berry", "Loc": "Routes 119, 123", "Effect": "Restores 25% HP", "Best": "Tanks"},
    "Lum Berry": {"Img": "lum-berry", "Loc": "Route 123", "Effect": "Cures any status", "Best": "All-rounders"}
}

# ניווט באמצעות טאבים (יציב יותר)
tab1, tab2 = st.tabs(["פוקדקס", "מדריך גרגירים"])

with tab1:
    @st.cache_data
    def get_pokemon_names():
        res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
        return [p['name'] for p in res.json()['results']]

    pokemon_names = get_pokemon_names()
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון:')

    if user_input:
        match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.3)
        name = match[0] if match else user_input.lower().strip()
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        
        if res.status_code == 200:
            data = res.json()
            species = requests.get(data['species']['url']).json()
            desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(data['sprites']['other']['official-artwork'].get('front_default'), width=300)
            with c2:
                st.subheader(f"פוקימון: {name.upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**מידע:** {desc}")
                if data['sprites'].get('front_shiny'):
                    st.image(data['sprites']['front_shiny'], width=100, caption="Shiny Form")
            
            tts = gTTS(text=f"Pokemon {name}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3")
    else:
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                st.markdown(f"**#{i}**")

with tab2:
    st.header("🍎 מדריך גרגירים")
    cols = st.columns(3)
    for i, (name, d) in enumerate(berries_data.items()):
        with cols[i % 3]:
            st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/items/{d['Img']}.png", width=100)
            st.subheader(name)
            with st.expander("ראה פרטים"):
                st.write(f"**איפה:** {d['Loc']}")
                st.write(f"**אפקט:** {d['Effect']}")
                st.write(f"**מתאים ל:** {d['Best']}")
