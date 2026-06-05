import streamlit as st
from gtts import gTTS
import requests
import difflib

# הגדרת דף
st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- מאגר נתונים לגרגירים ---
# וודא שהתמונות ב-GitHub שלך נקראות בדיוק כך:
berries_data = {
    "Oran": {"Img": "oran.png.png", "Effect": "משחזר 10 נקודות חיים (HP)."},
    "Sitrus": {"Img": "sitrus.png.png", "Effect": "משחזר 25% מהחיים המקסימליים."},
    "Lum": {"Img": "lum.png.png", "Effect": "מרפא כל סטטוס (הרעלה, שיתוק וכו')."},
    "Cheri": {"Img": "cheri.png.png", "Effect": "מרפא שיתוק (Paralysis)."},
    "Chesto": {"Img": "chesto.png.png", "Effect": "מעיר פוקימון שנרדם."}
}

regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

# --- תפריט צד ---
menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

# --- לוגיקת פוקדקס ---
if menu == "פוקדקס":
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון:')
    
    if user_input:
        match = difflib.get_close_matches(user_input.lower().strip(), pokemon_names, n=1, cutoff=0.3)
        name = match[0] if match else user_input.lower().strip()
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        
        if res.status_code == 200:
            data = res.json()
            species = requests.get(data['species']['url']).json()
            desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
            types = [t['type']['name'] for t in data['types']]
            
            # אוכל אהוב
            if "grass" in types: food = "פירות יער (Berries)"
            elif "water" in types: food = "פופינס (Poffins)"
            else: food = "אוכל מבושל באש"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                off = data['sprites']['other']['official-artwork'].get('front_default')
                st.image(off if off else data['sprites'].get('front_default'), width=300)
                shiny = data['sprites'].get('front_shiny')
                if shiny: st.image(shiny, width=150, caption="Shiny Form")
            
            with c2:
                st.subheader(f"פוקימון: {data['name'].upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                
            tts = gTTS(text=f"{data['name']}. {desc}", lang='en')
            tts.save("p.mp3")
            st.audio("p.mp3", autoplay=True)
            
    else:
        st.subheader(f"מחוז {selected_region}")
        start, end = regions[selected_region]
        cols = st.columns(6)
        for i in range(start, end + 1):
            with cols[(i - start) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png")
                p_res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
                st.markdown(f"**{p_res['name'].capitalize()}**")

# --- לוגיקת מדריך גרגירים ---
elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    cols = st.columns(len(berries_data))
    for i, (name, d) in enumerate(berries_data.items()):
        with cols[i]:
            try:
                st.image(d["Img"], width=100)
            except:
                st.write("תמונה חסרה")
            st.subheader(name)
            if st.button(f"שמע על {name}", key=name):
                tts = gTTS(text=f"{name} Berry. Effect: {d['Effect']}", lang='en')
                tts.save(f"audio_{name}.mp3")
                st.audio(f"audio_{name}.mp3", autoplay=True)
            st.write(d["Effect"])
