import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני מחוזות
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

# טאבים לניווט
tab1, tab2 = st.tabs(["פוקדקס", "מדריך גרגירים"])

with tab1:
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון (למשל: charizard):')

    if user_input:
        # לוגיקת חיפוש
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_input.lower().strip()}")
        if res.status_code == 200:
            data = res.json()
            species = requests.get(data['species']['url']).json()
            desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            types = [t['type']['name'] for t in data['types']]
            food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked food"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(data['sprites']['other']['official-artwork'].get('front_default'), width=300)
            with c2:
                st.subheader(data['name'].upper())
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                if data['sprites'].get('front_shiny'):
                    st.image(data['sprites']['front_shiny'], width=100, caption="Shiny Form")
            
            # אודיו אוטומטי
            tts = gTTS(text=f"{data['name']}. {desc}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
    else:
        # גלריה של כל המחוז
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
                st.image(img_url)
                # שליפת שם להצגה מתחת לתמונה
                p_res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
                st.markdown(f"**#{i} {p_res['name'].capitalize()}**")

with tab2:
    st.subheader("🍎 מדריך גרגירים")
    # כאן יופיע מדריך הגרגירים שלך
