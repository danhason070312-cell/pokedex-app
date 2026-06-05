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

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

menu = st.sidebar.radio("בחר:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
    user_input = st.text_input('חפש פוקימון (תיקון שגיאות פעיל):')

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
                # מנגנון הגנה: בודק אם יש תמונה רשמית, אם לא - משתמש בסטנדרטית
                official = data['sprites']['other']['official-artwork'].get('front_default')
                standard = data['sprites'].get('front_default')
                st.image(official if official else standard, width=300)
                
            with c2:
                st.subheader(f"פוקימון: {data['name'].upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                shiny = data['sprites'].get('front_shiny')
                if shiny: st.image(shiny, width=150, caption="Shiny Form")
            
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
                st.markdown(f"**#{i}**")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים מורחב")
    
    # מאגר גרגירים מעודכן עם מיקומים (מסלולים), אקלים והקראה
    berries_info = {
        "Oran": {"Loc": "מסלולים 102, 104, 111", "Climate": "אקלים ממוזג", "Effect": "משחזר 10 HP", "Best": "פוקימון שנפגע קלות"},
        "Sitrus": {"Loc": "מסלולים 119, 123", "Climate": "אקלים לח וטרופי", "Effect": "משחזר רבע מה-HP", "Best": "פוקימון הגנה"},
        "Lum": {"Loc": "מסלול 123", "Climate": "אקלים הררי גבוה", "Effect": "מרפא כל בעיה", "Best": "כל פוקימון"},
        "Cheri": {"Loc": "מסלולים 104, 115", "Climate": "אקלים שמש חזק", "Effect": "מרפא שיתוק", "Best": "פוקימון אש"}
    }
    
    selected = st.selectbox("בחר גרגיר למידע והקלטה:", list(berries_info.keys()))
    info = berries_info[selected]
    
    # תצוגה
    st.write(f"**מיקום:** {info['Loc']} (אלו המספרים של המסלולים שבהם אפשר למצוא אותם בעולם המשחק)")
    st.write(f"**אקלים:** {info['Climate']}")
    st.write(f"**השפעה:** {info['Effect']}")
    st.write(f"**מתאים ל:** {info['Best']}")
    
    # הקלטה אוטומטית לגרגיר
    tts_text = f"{selected} Berry. Found in {info['Loc']}. Climate: {info['Climate']}. Effect: {info['Effect']}"
    tts = gTTS(text=tts_text, lang='en')
    tts.save("berry.mp3")
    st.audio("berry.mp3", autoplay=True)
