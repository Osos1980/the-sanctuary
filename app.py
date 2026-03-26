import streamlit as st
import datetime
import random
import os

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    h1, h3 { color: #ff4b4b; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. JESSICA'S DATA ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. THE 8 AUDIO FILES (Confirmed from your latest list) ---
negan_playlist = [
    "all-you-gotta-do-is-answer-one-simple-question.mp3",
    "do-not-let-me-distract-you-young-man.mp3",
    "easy-peasy-lemon-squeezy.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
    "here-goes-pay-attention.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-m-negan.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
]

def play_negan_radio():
    """Selects a file and displays a VISIBLE audio player."""
    clip = random.choice(negan_playlist)
    if os.path.exists(clip):
        audio_file = open(clip, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')
        st.caption(f"📻 Radio Frequency: {clip[:20]}...")
    else:
        st.error(f"⚠️ Signal Lost: {clip} not found in root folder.")

# --- 4. HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica")

# Boss Mood
mood = st.session_state.boss_mood
if mood > 70: st.success(f"😎 Negan's proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 Negan's watching you, Jess ({mood}%)")
else: st.error(f"💀 Negan is PISSED, Jess ({mood}%)")

# --- 5. JESSICA'S MISSIONS ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
tasks = ["Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Drop-off", "Coffee", "Groceries", "Cleaning", "Pickup"]

for t in tasks:
    if st.button(f"✔️ COMPLETE: {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Objective Secured: {t}")
        # THIS IS THE FIX: The player will now appear right here
        play_negan_radio()

# --- 6. JESSICA'S VAULT (REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")

if st.sidebar.button("☕ Premium Coffee (20)"):
    if st.session_state.points >= 20: st.session_state.points -= 20
if st.sidebar.button("🍺 Cold Cider (40)"):
    if st.session_state.points >= 40: st.session_state.points -= 40
if st.sidebar.button("🦶 Foot Massage (80)"):
    if st.session_state.points >= 80: st.session_state.points -= 80
if st.sidebar.button("🍽️ Fancy Dinner (150)"):
    if st.session_state.points >= 150: st.session_state.points -= 150

st.sidebar.write("---")
if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.points = 0
    st.session_state.boss_mood = 50
    st.rerun()
