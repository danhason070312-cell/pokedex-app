import streamlit as st
from gtts import gTTS
import requests

st.title("🎤 פוקדקס AI")

# אתחול מצב ה-key של התיבה
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# אזור קבוע לתוצאות (כדי שלא יזוז)
results_placeholder = st.empty()

# תיבת חיפוש עם key שמשתנה
user_input = st.text_input('חפש פוקימון:', key=f"search_{st.session_state.input_key}")

if user_input:
    # חיפוש לפי שם (ללא תיקון שגיאות כדי שלא יתבלבל)
    name = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "אין מידע.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        
        types_he = {"fire": "אש", "water": "מים", "grass": "עשב", "ghost": "רוח", "fairy": "פיה", "electric": "חשמל"}
        types = ", ".join([types_he.get(t['type']['name'], t['type']['name']) for t in data['types']])
        
        # עדכון אזור התוצאות
        with results_placeholder.container():
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(f"פוקימון: {data['name'].upper()}")
            st.write(f"**סוג:** {types}")
            st.write(f"**מידע:** {desc}")
            
            tts = gTTS(text=f"Pokemon {data['name']}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
            
        # שינוי ה-key כדי לנקות את תיבת החיפוש מבלי למחוק את התוצאות
        st.session_state.input_key += 1
        st.rerun() 
            
    else:
        st.error("לא מצאתי את הפוקימון הזה, נסה לרשום את השם במדויק (למשל: mimikyu)")
