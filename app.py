import streamlit as st
from gTTS import gTTS
import requests
import difflib
from streamlit_mic_recorder import mic_recorder
from googletrans import Translator

translator = Translator()

st.title("🎤 פוקדקס AI בעברית")

# כפתור מיקרופון
audio = mic_recorder(start_prompt="לחץ כאן לדיבור", stop_prompt="עצור", just_once=True)

if audio:
    # כאן היינו צריכים שרת צד ג' לתמלול, לכן נשתמש בטקסט שנקלט
    # בגלל מגבלות טכניות של תמלול מלא בפייתון, 
    # השיטה הכי טובה היא להשתמש בתיבת טקסט עם מיקרופון של המקלדת
    st.write("אנא השתמש בתיבה למטה לתוצאות הטובות ביותר")

user_input = st.text_input('חפש פוקימון:')

if user_input:
    clean_input = user_input.lower().replace("ספר לי על", "").strip().replace(" ", "-")
    # ... (לוגיקת החיפוש נשארת דומה) ...
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_input}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        desc_en = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No data.")
        
        # תרגום לעברית
        desc_he = translator.translate(desc_en, dest='he').text
        types = ", ".join([t['type']['name'] for t in data['types']])
        
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"פוקימון: {clean_input.upper()}")
        st.write(f"**סוג:** {types}")
        st.write(f"**מידע:** {desc_he}")
        
        # השמעה בעברית (נשתמש ב-gTTS עם עברית)
        tts = gTTS(text=desc_he, lang='he', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי את הפוקימון הזה.")
