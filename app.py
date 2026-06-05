import streamlit as st
from gtts import gTTS
import requests
import difflib

st.set_page_config(layout="wide")
st.title("馃帳 驻讜拽讚拽住 AI")

# 专砖讬诪转 讻诇 讛砖诪讜转 诇转讬拽讜谉 讗讬讜转
@st.cache_data
def get_pokemon_names():
    res = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1300")
    return [p['name'] for p in res.json()['results']]

pokemon_names = get_pokemon_names()

# 讛讙讚专转 诪讞讜讝讜转
regions = {
    "Kanto": (1, 151), "Johto": (152, 251), "Hoenn": (252, 386),
    "Sinnoh": (387, 493), "Unova": (494, 649), "Kalos": (650, 721), "Alola": (722, 809)
}

st.sidebar.header("讘讞专 诪讞讜讝:")
selected_region = st.sidebar.selectbox("诪讞讜讝:", list(regions.keys()))
start_id, end_id = regions[selected_region]

# 驻讜谞拽爪讬讛 诇讞讬砖讜讘 讞讜诇砖讜转
def get_weaknesses(types):
    weaknesses = set()
    for t in types:
        res = requests.get(f"https://pokeapi.co/api/v2/type/{t}").json()
        for dmg in res['damage_relations']['double_damage_from']:
            weaknesses.add(dmg['name'])
    return ", ".join(weaknesses)

# 讞讬驻讜砖
user_input = st.text_input('讞驻砖 驻讜拽讬诪讜谉:')

if user_input:
    clean_input = user_input.lower().strip()
    match = difflib.get_close_matches(clean_input, pokemon_names, n=1, cutoff=0.3)
    name = match[0] if match else clean_input
    
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    
    if res.status_code == 200:
        data = res.json()
        species = requests.get(data['species']['url']).json()
        
        # 谞转讜谞讬诐
        types = [t['type']['name'] for t in data['types']]
        desc = next((e['flavor_text'] for e in species['flavor_text_entries'] if e['language']['name'] == 'en'), "No info.")
        weaknesses = get_weaknesses(types)
        food = "Berries" if "grass" in types else "Poffins" if "water" in types else "Fire-cooked meat"
        
        # 讛爪讙讛
        st.image(data['sprites']['other']['official-artwork']['front_default'] or data['sprites']['front_default'], width=300)
        st.subheader(f"驻讜拽讬诪讜谉: {name.upper()}")
        st.write(f"**诪讬讚注:** {desc}")
        st.write(f"**讙讜讘讛:** {data['height']/10} 诪讟专讬诐")
        st.write(f"**讗讜讻诇 讗讛讜讘:** {food}")
        st.write(f"**住讜讙讬诐 讗驻拽讟讬讘讬讬诐 谞讙讚讜 (讞讜诇砖讜转):** {weaknesses}")
        st.image(data['sprites']['front_shiny'], width=150, caption="Shiny Form")
        
        # 讗讜讚讬讜
        tts = gTTS(text=f"Pokemon {name}. {desc}", lang='en', slow=False)
        tts.save("pokedex.mp3")
        st.audio("pokedex.mp3", autoplay=True)
    else:
        st.error("诇讗 诪爪讗转讬.")
else:
    # 转爪讜讙转 诪讞讜讝
    st.subheader(f"讻诇 讛驻讜拽讬诪讜谞讬诐 讘诪讞讜讝 {selected_region}:")
    cols = st.columns(6)
    for i in range(start_id, end_id + 1):
        with cols[(i - start_id) % 6]:
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"
            st.image(img_url, use_column_width=True)
            st.markdown(f"**#{i}**")
