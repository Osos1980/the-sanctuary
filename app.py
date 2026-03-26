import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & PERSONALIZATION ---
st.set_page_config(page_title="The Sanctuary: Jessica's Command", page_icon="🏏", layout="centered")

# Custom CSS for Jessica's Saviors theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; border: 1px solid white; box-shadow: 0px 0px 15px #ff4b4b; }
    h1 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT DATA ---
if "points" not in st.session_state: st.session_state.points = 0
if "completed_today" not in st.session_state: st.session_state.completed_today = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. DATE & MISSION LOGIC ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

if is_work_day:
    tasks = ["Handover & Med Pass", "Charting (Stay sharp, Jess!)", "Hydration Break", "Final Safety Checks", "Decompression Drive"]
    header_msg = "🚨 FRONT LINE: HOSPITAL MISSION"
else:
    tasks = ["Kid Drop-off", "Coffee Recharge", "Scavenge (Groceries)", "Base Maintenance", "The Kid Pickup"]
    header_msg = "🏠 HOME BASE LOGISTICS"

# --- 4. THE JESSICA AUDIO ENGINE ---
# These match your latest file list exactly
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
    """Forces audio playback by creating a new audio element each time."""
    clip = random.choice(negan_playlist)
    if os.path.exists(clip):
        audio_file = open(clip, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.sidebar.error(f"Missing: {clip}")

# --- 5. INTERFACE ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica | **Status:** {today}")
if is_work_day: st.error(header_msg)
else: st.success(header_msg)

# Mood Indicator
mood = st.session_state.boss_mood
if mood > 75: st.success(f"😎 BOSS MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 BOSS MOOD: Watching your back, Jess ({mood}%)")
else: st.error(f"💀 BOSS MOOD: Don't make him ask twice, Jess ({mood}%)")

st.write("---")

# --- 6. MISSIONS ---
st.write("### 🎯 ACTIVE MISSIONS")
for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Objective Secured, Jess: {t}")
        play_negan()

# --- 7. REWARDS VAULT (SIDEBAR) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")

rewards = [
    ("☕ Premium Coffee", 20),
    ("🍺 Cold Cider", 40),
    ("🦶 Foot Massage", 80),
    ("🍽️ Fancy Dinner", 150),
    ("🛍️ Shopping Spree", 300)
]

for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.balloons()
            st.sidebar.success(f"CLAIMED: {name}")
        else:
            st.sidebar.error("Earn more points, Jessica.")

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.completed_today = 0
    st.session_state.boss_mood = 50
    st.rerun()
