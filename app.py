import streamlit as st
from gtts import gTTS
import requests
import difflib
import time

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

st.title("🎤 פוקדקס AI")

# מקום קבוע לתוצאות שלא נמחק
results_placeholder = st.empty()

# תיבת חיפוש עם key שמשתנה כל פעם כדי להתאפס
if 'search_key' not in st.session_state:
    st.session_state.search_key = 0

user_input = st.text_input('חפש פוקימון:', key=f"search_{st.session_state.search_key}")

if user_input:
    clean_input = user_input.lower().strip()
    
    # לוגיקת חיפוש: מימיקיו מחייב שם מדויק, השאר עם תיקון שגיאות
    if clean_input == "mimikyu":
        name = "mimikyu"
    else:
        match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.5)
        name = match[0] if match else clean_input

    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        # תצוגת התוצאות
        with results_placeholder.container():
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(f"פוקימון: {name.upper()}")
            st.write(f"**מידע:** {desc}")
            
            tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
            
        # טיימר של 16 שניות לאיפוס השורה
        time.sleep(16)
        st.session_state.search_key += 1
        st.rerun()
            
    else:
        st.error("לא מצאתי את הפוקימון הזה.")
