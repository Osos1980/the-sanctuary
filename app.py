import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; }
    .stTextInput>div>div>input { background-color: #1e2129; color: white; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "custom_tasks" not in st.session_state: st.session_state.custom_tasks = []

# --- 3. MASTER FILENAMES ---
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

def trigger_voice(command_key):
    mapping = {
        "easy": "easy-peasy-lemon-squeezy.mp3",
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "pick": "i-gotta-pick-somebody.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 4. HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### Commander: Jessica")

# --- 5. NEW: FIELD ORDERS (ADD CUSTOM TASKS) ---
st.write("---")
st.write("### 📝 NEW FIELD ORDERS")
new_task = st.text_input("What needs doing, Jessica?", placeholder="e.g., Extra Charting, Patient Move...")
if st.button("➕ ADD TO MISSION LOG"):
    if new_task:
        st.session_state.custom_tasks.append({"name": new_task, "done": False})
        st.toast(f"Task added: {new_task}")
        trigger_voice("question")
        # Clear the input by rerunning
        st.rerun()

# --- 6. MISSION LOG ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")

# Default Tasks
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
default_tasks = ["Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee", "Groceries", "Cleaning"]

# Combine Defaults + Jessica's Custom Tasks
for t in default_tasks:
    if st.button(f"✔️ {t}", key=f"default_{t}"):
        st.session_state.points += 20
        st.toast(f"Objective Secured: {t}")
        trigger_voice("random")

# Display Custom Tasks
for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ CUSTOM: {ct['name']}", key=f"custom_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30 # Custom tasks worth more!
            st.toast(f"Custom Objective Secured: {ct['name']}")
            trigger_voice("random")

# --- 7. SIDEBAR & RESET ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
if st.sidebar.button("🔄 CLEAR ALL & RESET"):
    st.session_state.points = 0
    st.session_state.custom_tasks = []
    st.rerun()
