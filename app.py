import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# מיפוי מחוזות מלא
regions = {
    "Kanto": (1, 151),
    "Johto": (152, 251),
    "Hoenn": (252, 386),
    "Sinnoh": (387, 493),
    "Unova": (494, 649),
    "Kalos": (650, 721),
    "Alola": (722, 809)
}

st.sidebar.header("בחר מחוז:")
selected_region = st.sidebar.selectbox("מחוז:", list(regions.keys()))
start_id, end_id = regions[selected_region]

user_input = st.text_input('חפש פוקימון:')

if user_input:
    # לוגיקת חיפוש חכם (נשארת זהה)
    name = user_input.lower().strip()
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if res.status_code == 200:
        data = res.json()
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"פוקימון: {data['name'].upper()}")
        st.write(f"**סוג:** {', '.join([t['type']['name'] for t in data['types']])}")
    else:
        st.error("לא נמצא.")
else:
    st.subheader(f"כל הפוקימונים במחוז {selected_region}:")
    
    # טעינה של כל הפוקימונים במחוז (ללא הגבלה של 12)
    # נשתמש ב-st.columns כדי להציג הכל בטבלה יפה
    pokemon_ids = range(start_id, end_id + 1)
    
    # הצגת הפוקימונים בגריד של 6 עמודות
    cols = st.columns(6)
    
    # נרוץ על כל המחוז (זה עשוי לקחת כמה שניות בטעינה הראשונה)
    for i in pokemon_ids:
        # שימוש ב-col דינמי
        with cols[(i - start_id) % 6]:
            # טעינה מהירה של ה-Sprite (תמונה קטנה)
            st.markdown(f"**#{i}**")
            # הוספנו קישור לתמונה
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
            st.image(img_url, use_column_width=True)
