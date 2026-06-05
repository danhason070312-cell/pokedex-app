import streamlit as st
from gtts import gTTS
import requests
import difflib

st.title("🎤 פוקדקס AI")

# רשימת שמות לתיקון איות
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

user_input = st.text_input('חפש פוקימון:')
results_placeholder = st.empty()

if user_input:
    clean_input = user_input.lower().strip()
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.4)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # בחירת תמונה בבטחה - אם אין artwork, נשתמש ב-front_default
        try:
            image_url = data['sprites']['other']['official-artwork']['front_default']
            if not image_url: raise Exception
        except:
            image_url = data['sprites']['front_default']
            
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        with results_placeholder.container():
            st.image(image_url, width=300)
            st.subheader(f"פוקימון: {name.upper()}")
            st.write(f"**מידע:** {desc}")
            
            tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
    else:
        results_placeholder.error("לא נמצא.")
