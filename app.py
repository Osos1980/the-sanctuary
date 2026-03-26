import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & PERSONALIZED STYLE ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; border: 1px solid white; box-shadow: 0px 0px 15px #ff4b4b; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT DATA (Jessica's Session) ---
if "points" not in st.session_state: st.session_state.points = 0
if "completed_today" not in st.session_state: st.session_state.completed_today = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. DATE & MISSION LOGIC ---
today = datetime.datetime.now().strftime("%A")
is_work_day = today in ["Friday", "Saturday", "Sunday"]

if is_work_day:
    tasks = ["Handover & Med Pass", "Charting (Stay sharp, Jess!)", "Hydration Break", "Final Safety Checks", "Drive Home Decompression"]
    status_color = "🚨"
else:
    tasks = ["Kid Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance", "The Kid Pickup"]
    status_color = "🏠"

# --- 4. THE NEGAN AUDIO ENGINE (Literal Filenames from Screenshot) ---
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

def trigger_audio():
    """Selects a random clip and displays it."""
    clip = random.choice(negan_playlist)
    if os.path.exists(clip):
        with open(clip, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    else:
        st.sidebar.error(f"Missing File: {clip}")

# --- 5. HEADER & BOSS MOOD ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica | **Status:** {today} {status_color}")

mood = st.session_state.boss_mood
if mood > 75: 
    st.success(f"😎 NEGAN'S MOOD: He's damn proud of you, Jess ({mood}%)")
elif mood > 40: 
    st.warning(f"😐 NEGAN'S MOOD: He's watching your back, Jess ({mood}%)")
else: 
    st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 6. RANDOM EVENTS (ADHD Dopamine Boost) ---
if random.random() < 0.15:
    event = random.choice([("SUPPLY DROP", 20, "🎁"), ("WALKERS AT THE GATE", -15, "🧟"), ("BONUS LOOT", 10, "💰")])
    st.info(f"{event[2]} EVENT: {event[0]}! Jessica's points adjusted by {event[1]}.")
    st.session_state.points += event[1]

# --- 7. MISSION CONTROL ---
st.write("---")
st.write("## 🎯 ACTIVE OBJECTIVES")

for t in tasks:
    if st.button(f"✔️ COMPLETE: {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Objective Secured: {t}")
        trigger_audio() # This puts the player right under the button!

# Progress Bar
progress_val = min(1.0, st.session_state.completed_today / len(tasks))
st.progress(progress_val)

# --- 8. TOOLS OF CHAOS ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        st.warning(f"JESSICA, DO THIS NOW: {random.choice(tasks)}")
        trigger_audio()
with c2:
    if st.button("⚡ JESS'S SPEED RUN"):
        st.error("⏱️ 10 MINUTES ON THE CLOCK. GO!")

# --- 9. THE VAULT (SIDEBAR REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Scavenge Points", f"{st.session_state.points} pts")
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

st.sidebar.write("---")
if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.completed_today = 0
    st.session_state.boss_mood = 50
    st.rerun()
