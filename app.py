import streamlit as st
from gtts import gTTS
import requests

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- הגדרת טאבים לניווט קבוע ---
tab1, tab2 = st.tabs(["פוקדקס", "מדריך גרגירים"])

with tab1:
    user_input = st.text_input('חפש פוקימון (למשל: charizard):')
    
    if user_input:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower().strip()}")
        if res.status_code == 200:
            data = res.json()
            
            # שליפת מידע מורחב (Species)
            species_res = requests.get(data['species']['url']).json()
            # חיפוש תיאור באנגלית
            desc = "No description available."
            for entry in species_res.get('flavor_text_entries', []):
                if entry['language']['name'] == 'en':
                    desc = entry['flavor_text']
                    break
            
            # חישוב אוכל אהוב (לפי סוג)
            types = [t['type']['name'] for t in data['types']]
            food = "Berries" if "grass" in types else "Fire-cooked food" if "fire" in types else "Poffins"
            
            # הצגת הנתונים עם הגנה
            col1, col2 = st.columns([1, 2])
            with col1:
                img = data['sprites']['other']['official-artwork'].get('front_default')
                if img: st.image(img, width=300)
            with col2:
                st.subheader(data['name'].upper())
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                
                # צורת שייני
                shiny = data['sprites'].get('front_shiny')
                if shiny:
                    st.image(shiny, width=100, caption="Shiny Form")
            
            # אודיו אוטומטי
            tts = gTTS(text=f"{data['name']}. {desc}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
        else:
            st.error("הפוקימון לא נמצא, נסה שם אחר.")

with tab2:
    st.subheader("🍎 מדריך גרגירים")
    # כאן תוכל להוסיף את רשימת הגרגירים שלך כפי שהיה
