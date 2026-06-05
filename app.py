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

berries_data = {
    "Oran Berry": {"Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/oran-berry.png", "Location": "מסלולים 102, 104, 111", "Effect": "משחזר 10 נקודות חיים (HP).", "Best For": "כל פוקימון שנפצע בקרב."},
    "Sitrus Berry": {"Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/sitrus-berry.png", "Location": "מסלולים 119, 123", "Effect": "משחזר רבע מכמות החיים המקסימלית.", "Best For": "פוקימוני הגנה (Tanks) שצריכים הישרדות."},
    "Lum Berry": {"Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/lum-berry.png", "Location": "מסלול 123", "Effect": "מרפא כל מצב סטטוס (הרעלה, שיתוק וכו').", "Best For": "פוקימונים רב-תכליתיים בקרבות."}
}

# --- לוגיקה ---
menu = st.sidebar.radio("בחר קטגוריה:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    @st.cache_data
    def get_pokemon_names():
        res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
        return [p['name'] for p in res.json()['results']]

    pokemon_names = get_pokemon_names()
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
            
            c1, c2 = st.columns(2)
            with c1:
                st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
            with c2:
                st.subheader(f"פוקימון: {name.upper()}")
                st.write(f"**גובה:** {data['height']/10} מטרים")
                st.write(f"**אוכל אהוב:** {food}")
                st.write(f"**מידע:** {desc}")
                st.image(data['sprites']['front_shiny'], width=100, caption="Shiny Form")
                
                tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
                tts.save("pokedex.mp3")
                st.audio("pokedex.mp3")
    else:
        st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
        start_id, end_id = regions[selected_region]
        cols = st.columns(6)
        for i in range(start_id, end_id + 1):
            with cols[(i - start_id) % 6]:
                st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png", use_column_width=True)
                st.markdown(f"**#{i}**")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים מלא")
    
    # הצגת כל הגרגירים בגלריה יפה
    cols = st.columns(3)
    for index, (name, details) in enumerate(berries_data.items()):
        with cols[index % 3]:
            st.image(details["Image"], width=120)
            st.subheader(name)
            with st.expander("לחץ לפרטים"):
                st.write(f"**איפה גדל:** {details['Location']}")
                st.write(f"**איך עוזר:** {details['Effect']}")
                st.write(f"**מתאים ל:** {details['Best For']}")
