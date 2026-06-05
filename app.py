import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני גרגירים
berries = {
    "Oran Berry": {"Effect": "החזרת HP", "Best For": "כל פוקימון שספג נזק"},
    "Sitrus Berry": {"Effect": "ריפוי משמעותי", "Best For": "פוקימוני הגנה (Tank)"},
    "Cheri Berry": {"Effect": "ריפוי שיתוק", "Best For": "פוקימוני אש או אדמה"},
    "Persim Berry": {"Effect": "ריפוי בלבול", "Best For": "פוקימונים מהירים (Sweepers)"},
    "Lum Berry": {"Effect": "ריפוי כל סטטוס", "Best For": "פוקימונים רב-תכליתיים"}
}

# תפריט צד - בחירת גרגיר
st.sidebar.header("מדריך גרגירים:")
selected_berry = st.sidebar.selectbox("בחר גרגיר:", list(berries.keys()))
st.sidebar.info(f"**השפעה:** {berries[selected_berry]['Effect']}\n\n**מתאים ל:** {berries[selected_berry]['Best For']}")

# --- (שאר הקוד נשאר כמו שהיה - חיפוש ומחוזות) ---

@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

user_input = st.text_input('חפש פוקימון:')

if user_input:
    clean_input = user_input.lower().strip()
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.3)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # נתונים
        types = [t['type']['name'] for t in data['types']]
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        
        # הצגה
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"פוקימון: {name.upper()}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.write(f"**סוג:** {', '.join(types)}")
        st.write(f"**מידע:** {desc}")
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
        
        # אודיו
        tts = gTTS(text=f"Pokemon {name}.", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי.")
