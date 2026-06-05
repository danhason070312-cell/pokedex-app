import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# רשימת כל השמות לתיקון איות
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

# הגדרת מחוזות
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

st.sidebar.header("בחר מחוז:")
selected_region = st.sidebar.selectbox("מחוז:", list(regions.keys()))
start_id, end_id = regions[selected_region]

# פונקציה לחישוב חולשות
def get_weaknesses(types):
    weaknesses = set()
    for t in types:
        res = requests.get(f"https://pokeapi.co/api/v2/type/{t}").json()
        for dmg in res['damage_relations']['double_damage_from']:
            weaknesses.add(dmg['name'])
    return ", ".join(weaknesses)

# חיפוש
user_input = st.text_input('חפש פוקימון:')

if user_input:
    clean_input = user_input.lower().strip()
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.3)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # נתונים
        types = [t['type']['name'] for t in data['types']]
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        weaknesses = get_weaknesses(types)
        food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked meat"
        
        # הצגה
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"פוקימון: {name.upper()}")
        st.write(f"**מידע:** {desc}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.write(f"**אוכל אהוב:** {food}")
        st.write(f"**סוגים אפקטיביים נגדו (חולשות):** {weaknesses}")
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
        
        # אודיו
        tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי.")
else:
    # תצוגת מחוז
    st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
    cols = st.columns(6)
    for i in range(start_id, end_id + 1):
        with cols[(i - start_id) % 6]:
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
            st.image(img_url, use_column_width=True)
            st.markdown(f"**#{i}**")
