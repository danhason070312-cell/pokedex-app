import streamlit as st
from gtts import gTTS
import requests
import difflib

# --- עיצוב CSS לניאון וממשק מודרני ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .card { border: 2px solid #00f2ff; border-radius: 15px; padding: 20px; background: #1a1c23; }
    .neon-text { color: #00f2ff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎤 AI Pokedex")

# (שאר המשתנים נשארים אותו דבר...)
# ... [העתק כאן את ה-berries_data וה-regions מהקוד הקודם] ...

# --- לוגיקת פוקדקס ---
if menu == "פוקדקס":
    user_input = st.text_input('Search Pokemon:')
    if user_input:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower()}")
        if res.status_code == 200:
            data = res.json()
            # הפעלה אוטומטית של קול (פייתון יקריא את המידע ברגע שהדף ייטען)
            desc = "A powerful electric pokemon." # כאן יבוא התיאור האמיתי מה-API
            tts = gTTS(text=desc, lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
            
            # הצגת המידע בתוך "כרטיס" מעוצב
            st.markdown(f"""
            <div class="card">
                <h2 class="neon-text">{data['name'].upper()}</h2>
                <p>Height: {data['height']/10}m | Weight: {data['weight']/10}kg</p>
                <p><b>Description:</b> {desc}</p>
                <p><i>(תיאור: פוקימון חשמל עוצמתי.)</i></p>
            </div>
            """, unsafe_allow_html=True)
