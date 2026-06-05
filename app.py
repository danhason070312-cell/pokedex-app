import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("🎤 פוקדקס AI")

# --- נתוני גרגירים מורחבים ---
berries_data = {
    "Oran Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/oran-berry.png",
        "Growth Location": "Route 102, 104, 111",
        "Effect": "משחזר 10 נקודות HP.",
        "Best For": "כל פוקימון שנפצע בקרב."
    },
    "Sitrus Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/sitrus-berry.png",
        "Growth Location": "Route 119, 123",
        "Effect": "משחזר רבע מכמות ה-HP המקסימלית.",
        "Best For": "פוקימוני הגנה (Tanks) שצריכים הישרדות."
    },
    "Lum Berry": {
        "Image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/items/lum-berry.png",
        "Growth Location": "Route 123",
        "Effect": "מרפא כל בעיית סטטוס (הרעלה, שיתוק וכו').",
        "Best For": "פוקימונים רב-תכליתיים בקרבות תחרותיים."
    }
}

# --- תפריט צד ---
st.sidebar.header("ניווט")
menu = st.sidebar.radio("בחר קטגוריה:", ["פוקדקס", "מדריך גרגירים"])

if menu == "מדריך גרגירים":
    st.header("🍎 מדריך גרגירים")
    selected_berry = st.selectbox("בחר גרגיר:", list(berries_data.keys()))
    
    # הצגת מידע מסודר
    berry = berries_data[selected_berry]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(berry["Image"], width=200)
    with col2:
        st.write(f"### {selected_berry}")
        st.write(f"**איפה גדל:** {berry['Growth Location']}")
        st.write(f"**איך עוזר:** {berry['Effect']}")
        st.write(f"**מתאים ל:** {berry['Best For']}")

else:
    # --- לוגיקת הפוקדקס (כמו שהיה) ---
    # [כאן תשאיר את הקוד של החיפוש והמחוזות כפי שהוא]
    st.write("ברוך הבא לפוקדקס! השתמש בתפריט הצד כדי לעבור למדריך הגרגירים.")
