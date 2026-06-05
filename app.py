import streamlit as st
from gtts import gTTS
import requests

st.title("🎤 פוקדקס AI")

# פונקציה להבאת סוגים חלשים (Type Effectiveness)
def get_weaknesses(types):
    weaknesses = set()
    for t in types:
        res = requests.get(f"https://pokeapi.co/api/v2/type/{t}").json()
        for dmg in res['damage_relations']['double_damage_from']:
            weaknesses.add(dmg['name'])
    return ", ".join(weaknesses)

user_input = st.text_input('חפש פוקימון:')

if user_input:
    name = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # איסוף נתונים
        types = [t['type']['name'] for t in data['types']]
        weaknesses = get_weaknesses(types)
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        
        # אוכל אהוב לפי סוג
        food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked food"
        
        # תצוגה
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.subheader(f"פוקימון: {data['name'].upper()}")
        
        # הנתונים שביקשת
        st.write(f"**מידע:** {desc}")
        st.write(f"**גובה:** {data['height']/10} מטרים")
        st.write(f"**סוג:** {', '.join(types)}")
        st.write(f"**סוגים אפקטיביים נגדו (חולשות):** {weaknesses}")
        st.write(f"**אוכל אהוב:** {food}")
        
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
        
        # אודיו
        tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("לא מצאתי.")
