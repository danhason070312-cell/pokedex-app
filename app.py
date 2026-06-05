import streamlit as st
from gtts import gTTS  # שים לב: gtts באותיות קטנות!
import requests

# כותרת ראשית
st.title("🎤 פוקדקס AI")

# תיבת חיפוש בראש העמוד
user_input = st.text_input('חפש פוקימון (נסה mimikyu):')

# מקום לתוצאות מתחת לתיבה
results_placeholder = st.empty()

if user_input:
    name = user_input.lower().strip()
    # חיפוש ב-API
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # איסוף נתונים
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        desc = desc.replace('\n', ' ').replace('\f', ' ')
        types = ", ".join([t['type']['name'] for t in data['types']])
        weight = data['weight'] / 10  # בקילוגרם
        height = data['height'] / 10  # במטרים
        
        # תצוגה
        with results_placeholder.container():
            st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
            st.subheader(f"פוקימון: {data['name'].upper()}")
            st.write(f"**סוג:** {types}")
            st.write(f"**גובה:** {height} מטרים")
            st.write(f"**משקל:** {weight} ק\"ג")
            st.write(f"**מידע:** {desc}")
            
            # אודיו
            tts = gTTS(text=f"Pokemon {data['name']}. Type {types}. {desc}", lang='en', slow=False)
            tts.save("pokedex.mp3")
            st.audio("pokedex.mp3", autoplay=True)
    else:
        results_placeholder.error("לא מצאתי את הפוקימון. וודא איות!")
