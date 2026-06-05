import streamlit as st
from gtts import gTTS
import requests
import difflib

# 1. טעינת רשימת כל הפוקימונים (פעם אחת בלבד)
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

st.title("🎤 פוקדקס AI")

# 2. תיבת חיפוש בראש
user_input = st.text_input('חפש פוקימון:')

results_placeholder = st.empty()

if user_input:
    clean_input = user_input.lower().strip()
    
    # 3. מציאת השם הכי קרוב (זה הפתרון לאיות לא מדויק)
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.3)
    name = match[0] if match else clean_input
    
    # חיפוש ב-API
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # איסוף נתונים
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        types = ", ".join([t['type']['name'] for t in data['types']])
        weight = data['weight'] / 10
        height = data['height'] / 10
        
        # תצוגה
        with results_placeholder.container():
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(f"פוקימון: {data['name'].upper()}")
            st.write(f"**סוג:** {types}")
            st.write(f"**גובה:** {height} מטרים")
            st.write(f"**משקל:** {weight} ק\"ג")
            st.write(f"**מידע:** {desc}")
            
            tts = gTTS(text=f"Pokemon {data['name']}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
    else:
        results_placeholder.error(f"לא מצאתי את הפוקימון {clean_input}. נסה שם אחר.")
