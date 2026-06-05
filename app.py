import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# מיפוי מחוזות למספרים ב-API
regions = {
    "Kanto": (1, 151),
    "Johto": (152, 251),
    "Hoenn": (252, 386),
    "Sinnoh": (387, 493),
    "Unova": (494, 649),
    "Kalos": (650, 721),
    "Alola": (722, 809)
}

# תפריט צד לבחירת מחוז
st.sidebar.header("בחר מחוז:")
selected_region = st.sidebar.selectbox("מחוז:", list(regions.keys()))
start_id, end_id = regions[selected_region]

# חיפוש חכם (נשאר אותו דבר)
user_input = st.text_input('חפש פוקימון:')

if user_input:
    # (הקוד של החיפוש נשאר כמו שסיכמנו קודם)
    pass 
else:
    st.subheader(f"פוקימונים במחוז {selected_region}:")
    
    # טעינת התמונות לפי מחוז
    cols = st.columns(6)
    for i in range(start_id, end_id + 1, 1): # טעינה הדרגתית
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
        
        # הצגת 12 פוקימונים ראשונים במחוז כדי לא להעמיס
        if i < start_id + 12:
            with cols[(i-start_id) % 6]:
                st.image(res['sprites']['front_default'], width=80)
                st.write(f"#{i} {res['name'].capitalize()}")
