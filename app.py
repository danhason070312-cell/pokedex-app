import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# נתוני מחוזות וגרגירים
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

berries_data = {
    "Oran Berry": {"Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/oran-berry.png", "Location": "מסלולים 102, 104", "Effect": "משחזר 10 HP", "Best For": "כל פוקימון"},
    "Sitrus Berry": {"Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/sitrus-berry.png", "Location": "מסלולים 119, 123", "Effect": "משחזר רבע מה-HP", "Best For": "פוקימוני הגנה"}
}

# תפריט צד - רק בשביל הגרגירים
st.sidebar.header("עזרים")
if st.sidebar.checkbox("הצג מדריך גרגירים"):
    st.sidebar.subheader("🍎 מדריך גרגירים")
    selected_berry = st.sidebar.selectbox("בחר גרגיר:", list(berries_data.keys()))
    berry = berries_data[selected_berry]
    st.sidebar.image(berry["Image"], width=100)
    st.sidebar.write(f"**איפה גדל:** {berry['Location']}")
    st.sidebar.write(f"**איך עוזר:** {berry['Effect']}")
    st.sidebar.write(f"**מתאים ל:** {berry['Best For']}")
    st.sidebar.markdown("---")

# לוגיקת הפוקדקס (הכל נשאר אותו דבר)
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()
selected_region = st.selectbox("בחר מחוז:", list(regions.keys()))
user_input = st.text_input('חפש פוקימון:')

if user_input:
    clean_input = user_input.lower().strip()
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.3)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if res.status_code == 200:
        data = res.json()
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"פוקימון: {name.upper()}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
else:
    st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
    start_id, end_id = regions[selected_region]
    cols = st.columns(6)
    for i in range(start_id, end_id + 1):
        with cols[(i - start_id) % 6]:
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
            st.image(img_url, use_column_width=True)
            st.markdown(f"**#{i}**")
