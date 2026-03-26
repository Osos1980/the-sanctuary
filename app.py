import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. VOICE COMMAND LOGIC ---
def trigger_voice(command_type):
    """Maps specific actions to the exact filenames from your 1:48 AM list."""
    commands = {
        "task_done": "easy-peasy-lemon-squeezy.mp3",
        "big_win": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
        "chaos": "i-gotta-pick-somebody.mp3",
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "warning": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3",
        "logic": "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
        "snark": "are-you-kidding-me.mp3",
        "serious": "i-think-it-would-be-enjoyable-screw-your-brains-out.mp3"
    }
    
    file = commands.get(command_type)
    if file and os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 4. HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica")

mood = st.session_state.boss_mood
if mood > 75: st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
else: st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 5. MISSIONS (With Voice Feedback) ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]

if is_work:
    tasks = ["Handover & Med Pass", "Charting", "Hydration Break", "Safety Checks", "Drive Home"]
else:
    tasks = ["Girls Drop-off", "Coffee Recharge", "Scavenge Run", "Base Maintenance", "Girls Pickup"]

for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Good work, Jessica.")
        # Play the 'Easy Peasy' command for every task
        trigger_voice("task_done")

# --- 6. CHAOS TOOLS ---
st.write("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏏 LUCILLE DECIDES"):
        trigger_voice("chaos")
        st.warning(f"JESSICA, DO THIS NOW: {random.choice(tasks)}")
with col2:
    if st.button("⚡ SPEED RUN"):
        trigger_voice("warning")
        st.error("⏱️ 10 MINUTES. GO!")

# --- 7. SIDEBAR RADIO & VAULT ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")

st.sidebar.write("---")
st.sidebar.write("### 🗣️ MANUAL COMMANDS")
if st.sidebar.button("Status Report"): trigger_voice("question")
if st.sidebar.button("The Reality Check"): trigger_voice("logic")
if st.sidebar.button("Negan's Approval"): trigger_voice("big_win")

st.sidebar.write("---")
if st.sidebar.button("🍺 Cider (40)"):
    if st.session_state.points >= 40:
        st.session_state.points -= 40
        st.sidebar.balloons()
if st.sidebar.button("🔄 RESET"):
    st.session_state.points = 0
    st.rerun()
