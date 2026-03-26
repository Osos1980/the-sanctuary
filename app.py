import streamlit as st
import datetime
import random
import os

# --- 1. SETTINGS ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. THE 9 FILENAMES (Literal from 1:48 AM Screenshot) ---
negan_playlist = [
    "all-you-gotta-do-is-answer-one-simple-question.mp3",
    "are-you-cooperating.mp3",
    "are-you-kidding-me.mp3",
    "do-not-let-me-distract-you-young-man.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
    "i-think-it-would-be-enjoyable-screw-your-brains-out.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
]

# --- 4. HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica")

# --- 5. THE RADIO (PLAY ALL MODE) ---
st.write("---")
st.write("### 📻 SAVIOR RADIO")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 RANDOM CLIP"):
        clip = random.choice(negan_playlist)
        if os.path.exists(clip):
            st.audio(open(clip, 'rb').read(), format='audio/mp3')
            st.caption(f"Playing: {clip[:30]}...")
        else:
            st.error("File not found. Check GitHub root.")

with col2:
    if st.button("📜 PLAY ALL IN ORDER"):
        st.info("Files loaded below. Scroll to play through the playlist!")
        for clip in negan_playlist:
            if os.path.exists(clip):
                st.write(f"**{clip.split('.')[0].replace('-', ' ').title()}**")
                st.audio(open(clip, 'rb').read(), format='audio/mp3')

# --- 6. MISSIONS ---
st.write("---")
st.write("### 🎯 OBJECTIVES")
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
tasks = ["Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Drop-off the girls", "Coffee", "Groceries", "Cleaning", "Pickup"]

for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.toast(f"Good work, Jessica.")
        # Play a random order after a task
        c = random.choice(negan_playlist)
        if os.path.exists(c):
            st.audio(open(c, 'rb').read(), format='audio/mp3')

# --- 7. VAULT ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
if st.sidebar.button("🍺 Cider (40)"):
    if st.session_state.points >= 40: st.session_state.points -= 40
if st.sidebar.button("🦶 Massage (80)"):
    if st.session_state.points >= 80: st.session_state.points -= 80
if st.sidebar.button("🍽️ Fancy Dinner (150)"):
    if st.session_state.points >= 150: st.session_state.points -= 150

if st.sidebar.button("🔄 RESET"):
    st.session_state.points = 0
    st.rerun()
