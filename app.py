import streamlit as st
import datetime
import random
import os

# --- CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

# --- SESSION STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "completed_today" not in st.session_state: st.session_state.completed_today = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- STYLE ---
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }
.stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DATE & TASKS ---
today = datetime.datetime.now().strftime("%a")
work_days = ["Fri", "Sat", "Sun"]
is_work_day = today in work_days
tasks = ["Handover/Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work_day else ["Drop-off", "Coffee", "Groceries", "Cleaning", "Pickup"]

# --- THE DEFINITIVE PLAYLIST (From your latest screenshot) ---
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

def play_negan():
    # Picks a random clip and plays it immediately
    clip = random.choice(negan_playlist)
    if os.path.exists(clip):
        with open(clip, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True)
    else:
        st.sidebar.error(f"Missing file: {clip}")

# --- HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### Mission Status: {today}")

# Boss Mood Display
if st.session_state.boss_mood > 70: st.success(f"😎 Mood: Chill ({st.session_state.boss_mood}%)")
elif st.session_state.boss_mood > 40: st.warning(f"😐 Mood: Watching ({st.session_state.boss_mood}%)")
else: st.error(f"💀 Mood: PISSED ({st.session_state.boss_mood}%)")

# --- MAIN CONTROLS ---
st.write("---")
if st.button("📢 HEAR THE BOSS (Sound Check)"):
    play_negan()

st.write("### 🎯 ACTIVE MISSIONS")
for t in tasks:
    if st.button(f"✔️ {t}", key=t):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        play_negan() # Plays every time she clicks a task!
        st.rerun()

# --- REWARDS SIDEBAR ---
st.sidebar.title("💎 VAULT")
st.sidebar.metric("Bank", f"{st.session_state.points} pts")
if st.sidebar.button("🍺 Cider (40)"): 
    if st.session_state.points >= 40: st.session_state.points -= 40
if st.sidebar.button("🦶 Massage (80)"): 
    if st.session_state.points >= 80: st.session_state.points -= 80
if st.sidebar.button("🍽️ Dinner (120)"): 
    if st.session_state.points >= 120: st.session_state.points -= 120

if st.sidebar.button("🔄 RESET"):
    st.session_state.completed_today = 0
    st.session_state.boss_mood = 50
    st.rerun()

# --- THE HIDDEN DEBUGGER ---
with st.expander("🛠️ Why is it silent? (Check filenames)"):
    st.write("Files GitHub sees right now:")
    st.write(os.listdir("."))
