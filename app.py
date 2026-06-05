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

# הוספתי כאן את שמות קבצי התמונה שהעלית (תצטרך לשמור אותם באותה תיקייה)
berries_data = {
    "Oran": {"Img": "image_7115db.png", "Effect": "משחזר 10 נקודות חיים (HP) מיידית בקרב."},
    "Sitrus": {"Img": "image_7118a5.png", "Effect": "משחזר 25% מהחיים המקסימליים של הפוקימון."},
    "Lum": {"Img": "image_7118ff.png", "Effect": "מרפא כל בעיית סטטוס: שיתוק, הרעלה, שינה, כוויה או קיפאון."},
    "Cheri": {"Img": "image_711939.png", "Effect": "מרפא שיתוק (Paralysis) ומחזיר את מהירות הפוקימון."},
    "Chesto": {"Img": "image_711978.png", "Effect": "מעיר את הפוקימון מיד במקרה שהוא נרדם בקרב."}
}

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()
menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

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
            food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked food"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                off = data['sprites']['other']['official-artwork'].get('front_default')
                st.image(off if off else data['sprites'].get('front_default'), width=300)
            with c2:
                st.subheader(f"פוקימון: {data['name'].upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                if data['sprites'].get('front_shiny'): st.image(data['sprites'].get('front_shiny'), width=150, caption="Shiny Form")
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
    
    # מיפוי השמות לקבצים שהעלית
    berries_data = {
        "Oran": {"Img": "image_7115db.png", "Effect": "משחזר 10 נקודות חיים (HP) מיידית."},
        "Sitrus": {"Img": "image_7118a5.png", "Effect": "משחזר 25% מהחיים המקסימליים של הפוקימון."},
        "Lum": {"Img": "image_7118ff.png", "Effect": "מרפא כל בעיית סטטוס: שיתוק, הרעלה, שינה, כוויה או קיפאון."},
        "Cheri": {"Img": "image_711939.png", "Effect": "מרפא שיתוק (Paralysis)."},
        "Chesto": {"Img": "image_711978.png", "Effect": "מעיר את הפוקימון מיד במקרה שנרדם."}
    }
    
    # תצוגת הגרגירים בשורה אחת
    cols = st.columns(len(berries_data))
    for i, (name, d) in enumerate(berries_data.items()):
        with cols[i]:
            st.image(d["Img"], width=100)
            st.subheader(name)
            st.write(d["Effect"])
            # כפתור הקראה עם טקסט מפורט ומדויק
            if st.button(f"שמע על {name}", key=name):
                tts = gTTS(text=f"{name} Berry effect is: {d['Effect']}", lang='en')
                tts.save("temp_berry.mp3")
                st.audio("temp_berry.mp3", autoplay=True)
