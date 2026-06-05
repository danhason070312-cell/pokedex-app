import streamlit as st
from gtts import gTTS
import requests
import difflib

# פונקציה לטעינת כל השמות לתיקון איות (מבוצע פעם אחת)
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

st.title("🎤 פוקדקס AI")

# פונקציה לחישוב חולשות
def get_weaknesses(types):
    weaknesses = set()
    for t in types:
        res = requests.get(f"https://pokeapi.co/api/v2/type/{t}").json()
        for dmg in res['damage_relations']['double_damage_from']:
            weaknesses.add(dmg['name'])
    return ", ".join(weaknesses)

# חיפוש
user_input = st.text_input('חפש פוקימון:')

if user_input:
    # תיקון איות: מוצא את השם הכי קרוב
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
        weaknesses = get_weaknesses(types)
        
        # הצגה
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"פוקימון: {name.upper()}")
        st.write(f"**סוג:** {', '.join(types)}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.write(f"**חולשות (אפקטיבי נגדו):** {weaknesses}")
        st.write(f"**מידע:** {desc}")
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
        
        # אודיו
        tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי את הפוקימון הזה.")
else:
    # תצוגת מסך הבית כשאין חיפוש
    st.subheader("פוקדקס - דפדוף מהיר:")
    cols = st.columns(4)
    for i, p in enumerate(pokemon_names[:12]): # מציג 12 ראשונים
        if i < 4:
            with cols[i % 4]:
                st.write(f"#{i+1} {p.capitalize()}")
