import streamlit as st
from gtts import gTTS
import requests
import difflib
import time

@st.cache_data
def get_pokemon_list():
    all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000").json()['results']
    return [p['name'] for p in all_pokemon]

pokemon_list = get_pokemon_list()

st.title("🎤 Pokédex AI")

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

user_input = st.textinput('Search Pokemon:', key=f"input{st.session_state.input_key}")

if user_input:
    clean_input = user_input.lower().replace("tell me about", "").strip().replace(" ", "-")
    match = difflib.get_close_matches(clean_input, pokemon_list, n=1, cutoff=0.6)
    name = match[0] if match else clean_input

    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/%7Bname%7D")

    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No data.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        types = ", ".join([t['type']['name'] for t in data['types']])

        st.subheader(f"POKÉDEX: {name.upper()}")
        st.write(f"Type: {types}")
        st.write(f"Info: {desc}")

יצירת האודיו
        tts = gTTS(text=f"Pokemon {name}. Type {types}. {desc}", lang='en', tld='co.uk', slow=False)
        tts.save("pokedex.mp3")

הצגת האודיו עם autoplay (הדפדפן יפעיל אותו מייד בגלל הלחיצה על ה-input)
        st.audio("pokedex.mp3", autoplay=True)

המתנה של 17 שניות ואז רענון של הדף לניקוי התיבה
        time.sleep(17)
        st.session_state.input_key += 1
        st.rerun()

    else:
        st.error(f"Could not find {name}.")
