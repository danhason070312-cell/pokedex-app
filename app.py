import streamlit as st
from gtts import gTTS
import requests
import difflib

# טעינת רשימת פוקימונים
@st.cache_data
def get_pokemon_list():
    all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000").json()['results']
    return [p['name'] for p in all_pokemon]

pokemon_list = get_pokemon_list()

st.title("Pokédex AI")
user_input = st.text_input('Type "Tell me about [name]"')

if user_input:
    clean_input = user_input.lower().replace("tell me about", "").strip().replace(" ", "-")
    match = difflib.get_close_matches(clean_input, pokemon_list, n=1, cutoff=0.5)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No data.")
        types = ", ".join([t['type']['name'] for t in data['types']])
        
        st.subheader(f"POKÉDEX: {name.upper()}")
        st.write(f"**Type:** {types}")
        st.write(f"**Info:** {desc}")
        
        tts = gTTS(text=f"Pokemon {name}. Type {types}. {desc}", lang='en', tld='co.uk', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3")
    else:
        st.error("Pokemon not found.")
