import streamlit as st
import random

st.title("🔫 Target Practice FPS")

if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.target_pos = random.randint(1, 10)

st.write(f"Target is at position: {st.session_state.target_pos}")
shot = st.number_input("Aim at position (1-10):", min_value=1, max_value=10, value=1)

if st.button("FIRE!"):
    if shot == st.session_state.target_pos:
        st.success("🎯 HEADSHOT! You hit the target.")
        st.session_state.score += 1
        st.session_state.target_pos = random.randint(1, 10)
        st.rerun()
    else:
        st.error("❌ Missed! Try again.")

st.write(f"### Current Score: {st.session_state.score}")
