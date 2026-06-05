import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- נתוני עזר ---
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

# טעינת שמות פוקימונים לחיפוש חכם
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

# תפריט ניווט
menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
  # תיקון בטיחות להצגת תמונה
            with c1:
                # מנסים קודם תמונה רשמית, אם אין - מנסים תמונה רגילה (sprite)
                img_url = data['sprites']['other']['official-artwork'].get('front_default')
                if not img_url:
                    img_url = data['sprites'].get('front_default')
                
                if img_url:
                    st.image(img_url, width=300)
                else:
                    st.write("תמונה לא זמינה")

    if user_input:
        # תיקון שגיאות כתיב
        match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.3)
        name = match[0] if match else user_input.lower().strip()
        
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        if res.status_code == 200:
            data = res.json()
            species = requests.get(data['species']['url']).json()
            
            # נתונים
            desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            types = [t['type']['name'] for t in data['types']]
            food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked food"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(data['sprites']['other']['official-artwork'].get('front_default'), width=300)
            with c2:
                st.subheader(f"פוקימון: {data['name'].upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                st.image(data['sprites'].get('front_shiny'), width=150, caption="Shiny Form")
            
            # אודיו אוטומטי
            tts = gTTS(text=f"{data['name']}. {desc}", lang='en', slow=False)
            tts.save("poke.mp3")
            st.audio("poke.mp3", autoplay=True)
            
    else:
        st.subheader(f"מחוז {selected_region}")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                p_res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
                st.markdown(f"**#{i} {p_res['name'].capitalize()}**")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    berries = {"Oran": "oran-berry", "Sitrus": "sitrus-berry", "Lum": "lum-berry"}
    cols = st.columns(3)
    for i, (name, img) in enumerate(berries.items()):
        with cols[i % 3]:
            st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/items/{img}.png", width=100)
            st.subheader(f"{name} Berry")
