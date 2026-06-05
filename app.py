import streamlit as st
from gtts import gTTS
import requests
import difflib

# טעינת רשימת פוקימונים (עם cache כדי שזה יעלה מהר)
@st.cache_data
def get_pokemon_list():
    all_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000").json()['results']
    return [p['name'] for p in all_pokemon]

pokemon_list = get_pokemon_list()

st.title("🎤 Pokédex AI")
st.write("לחץ על המיקרופון במקלדת ואמור: Tell me about Pikachu")

# התיבה שלנו
user_input = st.text_input('Search Pokemon:', key="input")

# אם יש תוכן בתיבה, נבצע את החיפוש
if user_input:
    # ניקוי הטקסט
    clean_input = user_input.lower().replace("tell me about", "").strip().replace(" ", "-")
    
    # תיקון שגיאות כתיב אוטומטי
    match = difflib.get_close_matches(clean_input, pokemon_list, n=1, cutoff=0.6)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No data.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        types = ", ".join([t['type']['name'] for t in data['types']])
        
        st.subheader(f"POKÉDEX: {name.upper()}")
        st.write(f"**Type:** {types}")
        st.write(f"**Info:** {desc}")
        
        # השמעה
        tts = gTTS(text=f"Pokemon {name}. Type {types}. {desc}", lang='en', tld='co.uk', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3")
    else:
        st.error(f"Could not find {name}. Please try again.")
