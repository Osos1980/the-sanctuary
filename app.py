import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; box-shadow: 0px 0px 15px #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    .stTextInput>div>div>input { background-color: #1e2129; color: white; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "custom_tasks" not in st.session_state: st.session_state.custom_tasks = []

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
] #

def trigger_voice(command_key):
    mapping = {
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "pick": "i-gotta-pick-somebody.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3",
        "cost": "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
        "cool": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 4. HEADER & DYNAMIC QUOTES ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica")

mood = st.session_state.boss_mood
if mood > 75: 
    st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
    st.info("Quote: 'I appreciate you, Jessica. Now get back to work.'")
elif mood > 40: 
    st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
    st.info("Quote: 'People are counting on you. Take it like a champ.'")
else: 
    st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")
    st.info("Quote: 'I hope you have your shitting pants on.'")

# --- 5. FIELD ORDERS (ADD OWN TASKS) ---
st.write("---")
st.write("### 📝 NEW FIELD ORDERS")
col_input, col_add = st.columns([3, 1])
with col_input:
    new_task = st.text_input("New objective:", placeholder="Enter custom task...", label_visibility="collapsed")
with col_add:
    if st.button("➕ ADD"):
        if new_task:
            st.session_state.custom_tasks.append({"name": new_task, "done": False})
            trigger_voice("question")
            st.rerun()

# --- 6. MISSION LOG ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")

today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
default_tasks = ["Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee", "Groceries", "Cleaning"]

# Show Defaults
for t in default_tasks:
    if st.button(f"✔️ {t}", key=f"def_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 5)
        st.toast(f"Secured: {t}")
        trigger_voice("random")

# Show Custom Tasks
for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ CUSTOM: {ct['name']}", key=f"cust_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30
            st.toast(f"Secured: {ct['name']}")
            trigger_voice("cool")

# --- 7. CHAOS TOOLS ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        trigger_voice("pick")
        st.warning(f"DO THIS NOW: {random.choice(default_tasks)}")
with c2:
    if st.button("⚡ SPEED RUN"):
        trigger_voice("die")
        st.error("⏱️ 10 MINUTES. GO!")

# --- 8. THE VAULT (REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
st.sidebar.write("---")

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

if st.sidebar.button("🔄 RESET ALL"):
    st.session_state.points = 0
    st.session_state.boss_mood = 50
    st.session_state.custom_tasks = []
    st.rerun()
