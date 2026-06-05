import streamlit as st
import requests

st.title("🎤 פוקדקס AI")

# פונקציה להבאת פרטים בסיסיים
def get_pokemon_info(name):
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    return res.json()

# 1. תצוגת מסך הבית (כשהחיפוש ריק)
def show_pokedex_grid():
    st.subheader("פוקדקס - דפדוף מהיר:")
    # מביא את 20 הפוקימונים הראשונים
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=20")
    pokemon_list = res.json()['results']
    
    cols = st.columns(4) # 4 עמודות בתצוגה
    for i, p in enumerate(pokemon_list):
        data = get_pokemon_info(p['name'])
        with cols[i % 4]:
            st.image(data['sprites']['front_default'], width=100)
            st.write(f"#{data['id']} {data['name'].capitalize()}")

# 2. לוגיקת החיפוש
user_input = st.text_input('חפש פוקימון:')

if not user_input:
    show_pokedex_grid()
else:
    # כאן נכנסת הלוגיקה הקודמת שלך לחיפוש ספציפי
    name = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if res.status_code == 200:
        data = res.json()
        # כאן הצגת המידע המלא כולל Shiny (זמין ב-API תחת sprites.front_shiny)
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=300)
        st.image(data['sprites']['front_shiny'], width=100, caption="Shiny Form")
        st.write(f"**סוג:** {', '.join([t['type']['name'] for t in data['types']])}")
    else:
        st.error("לא נמצא.")
