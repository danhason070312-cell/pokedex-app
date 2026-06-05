import streamlit as st
from gtts import gTTS
import requests

st.title("🎤 פוקדקס AI")

user_input = st.text_input('חפש פוקימון (באנגלית):')

if user_input:
    clean_input = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_input}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # תיאור באנגלית
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        # תרגום בסיסי לסוגים (Types)
        type_map = {
            "grass": "עשב", "fire": "אש", "water": "מים", "bug": "חרק", "normal": "נורמלי",
            "poison": "רעל", "electric": "חשמל", "ground": "אדמה", "fairy": "פיה", "fighting": "לחימה",
            "psychic": "על-חושי", "rock": "סלע", "ghost": "רוח", "ice": "קרח", "dragon": "דרקון"
        }
        types_en = [t['type']['name'] for t in data['types']]
        types_he = [type_map.get(t, t) for t in types_en]
        
        # הצגת תוצאות
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"פוקימון: {data['name'].upper()}")
        st.write(f"**סוג:** {', '.join(types_he)}")
        st.write(f"**מידע (באנגלית):** {desc}")
        
        # השמעה (נשאיר באנגלית כדי שזה לא יקרא ג'יבריש בעברית)
        tts = gTTS(text=f"Pokemon {data['name']}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("הפוקימון לא נמצא, נסה שוב.")
