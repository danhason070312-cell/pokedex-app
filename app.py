import streamlit as st
from gtts import gTTS
import requests
import difflib

# נגדיל את הלימיט כדי לתפוס את כל הפוקימונים
@st.cache_data
def get_pokemon_names():
    # הגדלנו את הלימיט ל-1300 כדי להבטיח שמימיקיו וכל השאר יופיעו
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

st.title("🎤 פוקדקס AI")

# מקום קבוע לתוצאות
results_container = st.empty()

user_input = st.text_input('חפש פוקימון:', key="search_box")

if user_input:
    match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.4)
    name = match[0] if match else user_input.lower().strip()
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "אין מידע.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        types_he = {"fire": "אש", "water": "מים", "grass": "עשב", "ghost": "רוח", "fairy": "פיה", "electric": "חשמל", "psychic": "על-חושי", "normal": "נורמלי", "dark": "אופל", "steel": "מתכת"}
        types = ", ".join([types_he.get(t['type']['name'], t['type']['name']) for t in data['types']])
        
        # הצגת המידע בתוך ה-container כך שהוא לא ימחק כשמשנים את התיבה
        with results_container.container():
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(f"פוקימון: {name.upper()}")
            st.write(f"**סוג:** {types}")
            st.write(f"**גובה:** {data['height']/10} מטרים")
            st.write(f"**מידע:** {desc}")
            
            # השמעה
            tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
            
    else:
        results_container.error("לא מצאתי את הפוקימון הזה, נסה שוב!")

# כדי לנקות את התיבה בלי למחוק את התוצאות, 
# אנחנו לא נשתמש ב-rerun, המשתמש פשוט יקליד מחדש והתוצאה תתעדכן מעצמה
