import streamlit as st
import requests
import difflib

# הגדרות עמוד
st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

@st.cache_data
def get_all_pokemon():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100") # הגדל ל-1000 אם צריך
    return res.json()['results']

all_pokemon = get_all_pokemon()

# תיבת חיפוש
user_input = st.text_input('חפש פוקימון (חיפוש חכם):')

if user_input:
    # חיפוש חכם עם תיקון איות
    names = [p['name'] for p in all_pokemon]
    match = difflib.get_close_matches(user_input.lower().strip(), names, n=1, cutoff=0.3)
    name = match[0] if match else user_input.lower().strip()
    
    # הצגת פוקימון בודד (הקוד שהיה לנו)
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if res.status_code == 200:
        data = res.json()
        st.image(data['sprites']['other']['official-artwork']['front_default'], width=200)
        st.write(f"### {name.upper()}")
        st.write(f"**סוג:** {', '.join([t['type']['name'] for t in data['types']])}")
    else:
        st.error("לא נמצא.")
else:
    # מסך בית - גלריה של פוקימונים
    st.subheader("כל הפוקימונים:")
    
    # חלוקה ל-6 עמודות למראה של פוקדקס אמיתי
    cols = st.columns(6)
    for i, p in enumerate(all_pokemon):
        # טעינת נתונים בסיסיים לכל פוקימון
        # הערה: בגלל כמות הנתונים, אנחנו מציגים רק שם כרגע למהירות
        with cols[i % 6]:
            st.markdown(f"**{i+1}.** {p['name'].capitalize()}")
