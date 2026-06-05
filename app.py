import streamlit as st
from gtts import gTTS
import requests

st.title("🎤 Pokédex AI")

user_input = st.text_input('Search Pokemon:')

if user_input:
    clean_input = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_input}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # תיאור באנגלית (הכי יציב)
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info available.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        types = ", ".join([t['type']['name'] for t in data['types']])
        
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"Name: {data['name'].upper()}")
        st.write(f"**Type:** {types}")
        st.write(f"**Info:** {desc}")
        
        # השמעה באנגלית
        tts = gTTS(text=f"Pokemon {data['name']}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("Pokemon not found.")
