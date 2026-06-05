import streamlit as st
from gtts import gTTS
import requests
import difflib
from deep_translator import GoogleTranslator

st.title("🎤 פוקדקס AI בעברית")

user_input = st.text_input('חפש פוקימון:')

if user_input:
    clean_input = user_input.lower().replace("ספר לי על", "").strip().replace(" ", "-")
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_input}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # שליפת תיאור באנגלית
        desc_en = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No data.")
        
        # תרגום לעברית באמצעות deep-translator
        desc_he = GoogleTranslator(source='en', target='he').translate(desc_en)
        types = ", ".join([t['type']['name'] for t in data['types']])
        
        # הצגת תוצאות
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"פוקימון: {clean_input.upper()}")
        st.write(f"**סוג:** {types}")
        st.write(f"**מידע:** {desc_he}")
        
        # השמעה בעברית
        tts = gTTS(text=desc_he, lang='he', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי את הפוקימון הזה.")
