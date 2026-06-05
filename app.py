import streamlit as st
from gtts import gTTS
import requests
import difflib
import time

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני עזר
regions = {"Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386), "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)}

# פונקציית ניקוי חיפוש
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# תפריט צד
st.sidebar.header("ניווט")
view_mode = st.sidebar.radio("מצב תצוגה:", ["פוקדקס", "מדריך גרגירים"])

if view_mode == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    # כאן יבוא הקוד של הגרגירים...
else:
    # לוגיקת פוקדקס
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    
    # שורת חיפוש עם מנגנון ניקוי
    user_input = st.text_input('חפש פוקימון:', key="search_query")
    
    if user_input:
        # הקפצה לניקוי אחרי 16 שניות
        time.sleep(16)
        st.session_state.search_query = ""
        st.rerun()

    # אם יש חיפוש -> תצוגת פוקימון בודד
    if user_input:
        # ... (לוגיקת החיפוש שלך)
        # בהצגת האודיו תשתמש ב: st.audio("pokedex.mp3", autoplay=True)
        pass
    else:
        # גלריה עם שמות
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                # הוספת השם מתחת למספר
                res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
                st.markdown(f"**#{i} {res['name'].capitalize()}**")
