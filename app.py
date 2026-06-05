import streamlit as st
from gtts import gTTS
import requests
import difflib

# רשימת כל השמות כדי שנוכל לתקן שגיאות כתיב
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

st.title("🎤 פוקדקס AI")

# ניהול מצב התיבה לאיפוס
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

user_input = st.text_input('חפש פוקימון (דבר למיקרופון במקלדת):', key=f"input_{st.session_state.input_key}")

if user_input:
    # תיקון שגיאות כתיב (כאן Mimikyu יימצא גם אם תכתוב Mimiky)
    match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.5)
    name = match[0] if match else user_input.lower().strip()
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # תיאור באנגלית
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "אין מידע זמין.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        # מילון עברית מורחב
        types_he = {"fire": "אש", "water": "מים", "grass": "עשב", "ghost": "רוח", "fairy": "פיה", "electric": "חשמל", "psychic": "על-חושי", "normal": "נורמלי"}
        types = ", ".join([types_he.get(t['type']['name'], t['type']['name']) for t in data['types']])
        
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"פוקימון: {name.upper()}")
        st.write(f"**סוג:** {types}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.write(f"**מידע:** {desc}")
        
        # הקראה באנגלית (כי זה נשמע הכי טבעי)
        tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
        
        # איפוס התיבה
        st.session_state.input_key += 1
        st.rerun()
    else:
        st.error("לא מצאתי את הפוקימון. נסה שוב!")
