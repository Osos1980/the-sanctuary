import streamlit as st
import datetime
import random
import os

# --- CONFIG ---
st.set_page_config(page_title="The Sanctuary: Survival Mode", page_icon="🏏", layout="centered")

# --- SESSION STATE INIT (Persistent Tracking) ---
if "points" not in st.session_state:
    st.session_state.points = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "completed_today" not in st.session_state:
    st.session_state.completed_today = 0
if "boss_mood" not in st.session_state:
    st.session_state.boss_mood = 50 

# --- STYLE ---
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }
.stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; margin-bottom: 10px; }
.stProgress > div > div > div > div { background-color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# --- DATE LOGIC ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- TASK SETS ---
work_tasks = ["Handover & Med Pass", "Charting", "Hydration Break", "Safety Checks", "Drive Home Decompression"]
home_tasks = ["Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance (Cleaning)", "The Kid Pickup"]
tasks = work_tasks if is_work_day else home_tasks

# --- FULL AUDIO PLAYLIST (Mapped from your screenshots) ---
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

def play_audio():
    # 60% chance to play a sound on click
    if random.random() < 0.6:
        clip = random.choice(negan_playlist)
        if os.path.exists(clip):
            with open(clip, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        else:
            st.sidebar.error(f"Missing File: {clip}")

# --- HEADER & MOOD ---
st.title("🏏 THE SANCTUARY")
st.write(f"### Mission Date: {today}")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.boss_mood > 75:
        st.success(f"😎 BOSS MOOD: CHILL ({st.session_state.boss_mood}%)")
    elif st.session_state.boss_mood > 40:
        st.warning(f"😐 BOSS MOOD: WATCHING ({st.session_state.boss_mood}%)")
    else:
        st.error(f"💀 BOSS MOOD: PISSED ({st.session_state.boss_mood}%)")

with col2:
    st.metric("STREAK", f"{st.session_state.streak} Days")

# --- RANDOM EVENTS ---
if random.random() < 0.20:
    event = random.choice([
        ("SUPPLY DROP", 20, "🎁"),
        ("WALKERS AT THE GATE", -15, "🧟"),
        ("BONUS LOOT", 10, "💰")
    ])
    st.info(f"{event[2]} EVENT: {event[0]}! Points adjusted by {event[1]}.")
    st.session_state.points += event[1]

# --- MISSIONS ---
st.write("---")
st.write("## 🎯 ACTIVE MISSIONS")

for task in tasks:
    if st.button(f"✔️ {task}", key=task):
        st.session_state.points += 20
        st.session_state.completed_today += 1
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 8)
        st.toast(f"Objective Secured: {task}")
        play_audio()

# --- PROGRESS ---
progress_val = min(1.0, st.session_state.completed_today / len(tasks))
st.progress(progress_val)

# --- LUCILLE & SPEED RUN ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        action = random.choice(["DO THIS NOW: " + random.choice(tasks), "DROP EVERYTHING → HYDRATE", "5 MIN SPEED CLEAN", "TAKE A BREAK"])
        st.error(action)
        play_audio()
with c2:
    if st.button("⚡ SPEED RUN (10 MIN)"):
        st.warning("⏱️ GO! Set a timer for 10 minutes. DO NOT STOP.")

# --- SIDEBAR REWARDS ---
st.sidebar.title("💎 THE VAULT")
st.sidebar.metric("Current Points", st.session_state.points)

st.sidebar.write("### Unlocked Spoils")
if st.sidebar.button("🍺 Use 40pts: Cold Cider"):
    if st.session_state.points >= 40: st.session_state.points -= 40
if st.sidebar.button("🦶 Use 80pts: Foot Massage"):
    if st.session_state.points >= 80: st.session_state.points -= 80
if st.sidebar.button("🍽️ Use 120pts: Fancy Dinner"):
    if st.session_state.points >= 120: st.session_state.points -= 120

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.completed_today = 0
    st.session_state.boss_mood = 50
    st.rerun()
