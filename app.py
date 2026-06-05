import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- נתוני גרגירים (עברית) ---
berries_data = {
    "Oran Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/oran-berry.png",
        "Growth Location": "מסלולים 102, 104, 111",
        "Effect": "משחזר 10 נקודות חיים (HP).",
        "Best For": "כל פוקימון שנפצע בקרב."
    },
    "Sitrus Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/sitrus-berry.png",
        "Growth Location": "מסלולים 119, 123",
        "Effect": "משחזר רבע מכמות החיים המקסימלית.",
        "Best For": "פוקימוני הגנה שצריכים הישרדות."
    },
    "Lum Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/lum-berry.png",
        "Growth Location": "מסלול 123",
        "Effect": "מרפא כל מצב סטטוס (הרעלה, שיתוק וכו').",
        "Best For": "פוקימונים רב-תכליתיים בקרבות."
    }
}

# --- לוגיקת ניווט ---
menu = st.sidebar.radio("בחר קטגוריה:", ["פוקדקס", "מדריך גרגירים"])

if menu == "פוקדקס":
    st.header("חיפוש פוקימונים")
    # [כאן הוסף את לוגיקת החיפוש והמחוזות שלך...]
    user_input = st.text_input('חפש פוקימון:')
    if user_input:
        st.write("מציג תוצאות עבור:", user_input)
        # תוסיף כאן את שארית הלוגיקה שלך מהקוד הקודם שעבדה
    else:
        st.write("בחר מחוז מהתפריט או חפש פוקימון.")

elif menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    selected_berry = st.selectbox("בחר גרגיר:", list(berries_data.keys()))
    
    berry = berries_data[selected_berry]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(berry["Image"], width=200)
    with col2:
        st.write(f"### {selected_berry}")
        st.write(f"**איפה גדל:** {berry['Growth Location']}")
        st.write(f"**איך עוזר:** {berry['Effect']}")
        st.write(f"**מתאים ל:** {berry['Best For']}")
