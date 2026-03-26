import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff3333; box-shadow: 0px 0px 15px #ff4b4b; transform: scale(1.02); }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "completed_today" not in st.session_state: st.session_state.completed_today = 0

# --- 3. THE 9 LITERAL FILENAMES (From 1:48 AM Screenshot) ---
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
    """Maps actions to specific audio clips."""
    mapping = {
        "easy": "easy-peasy-lemon-squeezy.mp3", # Note: Ensure this exists or it defaults to random
        "cool": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
        "pick": "i-gotta-pick-somebody.mp3",
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3",
        "cost": "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
        "kidding": "are-you-kidding-me.mp3",
        "brains": "i-think-it-would-be-enjoyable-screw-your-brains-out.mp3",
        "cooperate": "are-you-cooperating.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')
    else:
        st.sidebar.error(f"Missing: {file}")

# --- 4. DATE & TASK LOGIC ---
today = datetime.datetime.now().strftime("%A")
is_work_day = today in ["Friday", "Saturday", "Sunday"]

if is_work_day:
    tasks = ["Handover & Med Pass", "Charting (Stay sharp, Jess!)", "Hydration Break", "Safety Checks", "Drive Home Decompression"]
    header_msg = "🚨 MISSION: THE FRONT LINES"
else:
    tasks = ["Girls Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance", "The Girls Pickup"]
    header_msg = "🏠 MISSION: HOME BASE"

# --- 5. HEADER & BOSS MOOD ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica | **Status:** {today}")
st.error(header_msg) if is_work_day else st.success(header_msg)

# Dynamic Mood Quotes
mood = st.session_state.boss_mood
if mood > 75: st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
else: st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 6. 📻 VOICE COMMAND CENTER ---
st.write("---")
st.write("### 📻 SAVIOR RADIO")
vcol1, vcol2, vcol3 = st.columns(3)
with vcol1:
    if st.button("📢 STATUS"): trigger_voice("question")
with vcol2:
    if st.button("📢 REALITY"): trigger_voice("cost")
with vcol3:
    if st.button("📢 COOPERATE?"): trigger_voice("cooperate")

# --- 7. ACTIVE OBJECTIVES ---
st.write("---")
st.write("### 🎯 MISSION LOG")
for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Objective Secured, Jessica.")
        trigger_voice("cool" if st.session_state.completed_today >= 4 else "easy")

# Progress bar
st.progress(min(1.0, st.session_state.completed_today / len(tasks)))

# --- 8. CHAOS TOOLS ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        trigger_voice("pick")
        st.warning(f"JESSICA, DO THIS NOW: {random.choice(tasks)}")
with c2:
    if st.button("⚡ JESS'S SPEED RUN"):
        trigger_voice("die")
        st.error("⏱️ 10 MINUTES. GO!")

# --- 9. THE VAULT (SIDEBAR) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Scavenge Points", f"{st.session_state.points} pts")
st.sidebar.write("---")

rewards = [("☕ Coffee", 20), ("🍺 Cider", 40), ("🦶 Massage", 80), ("🍽️ Dinner", 150), ("🛍️ Shopping", 300)]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.balloons()
            st.sidebar.success(f"ENJOY, JESS: {name}")
        else: st.sidebar.error("Earn more points, Jessica.")

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.points = 0
    st.session_state.boss_mood = 50
    st.session_state.completed_today = 0
    st.rerun()
