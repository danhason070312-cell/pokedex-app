import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- הגדרת נתונים (גלובלי) ---
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

# --- תפריט ---
menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    # החזרתי את הפוקדקס המקורי שלך בדיוק כפי שהיה
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
            
            c1, c2 = st.columns([1, 2])
            with c1:
                off = data['sprites']['other']['official-artwork'].get('front_default')
                st.image(off if off else data['sprites'].get('front_default'), width=300)
            with c2:
                st.subheader(f"פוקימון: {data['name'].upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
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
                st.markdown(f"#{i}")

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
                tts.save("b.mp3")
                st.audio("b.mp3", autoplay=True)
            st.write(d["Effect"])
