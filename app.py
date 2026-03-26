import streamlit as st
import datetime
import random
import os

# --- 1. SETTINGS & INTERFACE ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 4em; font-weight: bold; border: none; font-size: 18px; }
    .stButton>button:hover { background-color: #ff3333; box-shadow: 0px 0px 20px #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "completed_today" not in st.session_state: st.session_state.completed_today = 0

# --- 3. MASTER FILENAMES (Verified from 1:48 AM Screenshot) ---
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
        "easy": "easy-peasy-lemon-squeezy.mp3", # Fallback if random
        "cool": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
        "pick": "i-gotta-pick-somebody.mp3",
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3",
        "cost": "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
        "cooperate": "are-you-cooperating.mp3",
        "kidding": "are-you-kidding-me.mp3",
        "brains": "i-think-it-would-be-enjoyable-screw-your-brains-out.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        audio_file = open(file, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')
    else:
        st.sidebar.error(f"⚠️ Signal Lost: {file}")

# --- 4. DATE & FRIDAY LOGIC ---
today = datetime.datetime.now().strftime("%A")
is_work_day = today in ["Friday", "Saturday", "Sunday"]

if is_work_day:
    tasks = ["Handover & Med Pass", "Charting (Stay sharp, Jess!)", "Hydration Break", "Safety Checks", "Drive Home Decompression"]
    mission_type = "🚨 HOSPITAL FRONT LINES"
else:
    tasks = ["Girls Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance", "The Girls Pickup"]
    mission_type = "🏠 HOME BASE LOGISTICS"

# --- 5. HEADER & PERSONALIZED QUOTES ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica | **Status:** {today}")
st.write(f"**Current Mission:** {mission_type}")

# Boss Mood Quotes
mood = st.session_state.boss_mood
if mood > 75: 
    st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: 
    st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
else: 
    st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 6. 📻 SAVIOR RADIO (VOICE COMMANDS) ---
st.write("---")
st.write("### 📻 VOICE COMMAND CENTER")
v1, v2, v3 = st.columns(3)
with v1:
    if st.button("📢 STATUS"): trigger_voice("question")
with v2:
    if st.button("📢 REALITY"): trigger_voice("cost")
with v3:
    if st.button("📢 COOPERATE"): trigger_voice("cooperate")

# --- 7. MISSION LOG (TASK LOOP) ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")
for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Objective Secured: {t}")
        # Play feedback sound
        trigger_voice("cool" if st.session_state.completed_today >= 4 else "brains")

st.progress(min(1.0, st.session_state.completed_today / len(tasks)))

# --- 8. CHAOS TOOLS ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        trigger_voice("pick")
        st.warning(f"JESSICA, DO THIS NOW: {random.choice(tasks)}")
with c2:
    if st.button("⚡ SPEED RUN"):
        trigger_voice("die")
        st.error("⏱️ 10 MINUTES ON THE CLOCK. GO!")

# --- 9. THE VAULT (REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Scavenge Points", f"{st.session_state.points} pts")
st.sidebar.write("---")

rewards = [("☕ Coffee", 20), ("🍺 Cider", 40), ("🦶 Massage", 80), ("🍽️ Dinner", 150), ("🛍️ Shopping", 300)]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.balloons()
            st.sidebar.success(f"CLAIMED: {name}")
        else:
            st.sidebar.error("Earn more points, Jessica.")

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.points = 0
    st.session_state.boss_mood = 50
    st.session_state.completed_today = 0
    st.rerun()
