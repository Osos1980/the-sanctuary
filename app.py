import streamlit as st
import datetime
import pytz 
import random
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff3333; box-shadow: 0px 0px 15px #ff4b4b; transform: scale(1.02); }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; text-align: center; }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    .streak-box { text-align: center; padding: 10px; border: 2px solid #ff4b4b; border-radius: 15px; margin-bottom: 20px; background: #1e2129; }
    .quote-box { padding: 15px; border-left: 5px solid #ff4b4b; background-color: #1e2129; font-style: italic; margin-bottom: 20px; border-radius: 0 10px 10px 0; }
    .bonus-locked { color: #555; font-style: italic; text-align: center; font-size: 0.9em; border: 1px dashed #444; padding: 10px; border-radius: 10px; }
    .bonus-unlocked { color: #00ff00; font-weight: bold; text-align: center; border: 2px solid #00ff00; padding: 10px; border-radius: 10px; background: #002200; animation: pulse 2s infinite; }
    @keyframes pulse { 0% {box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.4);} 70% {box-shadow: 0 0 0 10px rgba(0, 255, 0, 0);} 100% {box-shadow: 0 0 0 0 rgba(0, 255, 0, 0);} }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CENTRAL TIME LOGIC ---
central = pytz.timezone('US/Central')
now_central = datetime.datetime.now(central)
today_date = now_central.date()
current_hour = now_central.hour
current_day = now_central.strftime("%A")

# --- 3. PERSISTENT STATE ---
states = {
    "points": 0, "custom_tasks": [], "completed_defaults": [], 
    "streak": 0, "best_streak": 0, "last_completion_date": None
}
for key, val in states.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 4. DATA & AUDIO ---
is_work = current_day in ["Friday", "Saturday", "Sunday"]
defaults = ["Handover & Meds", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee Recharge", "Groceries", "Base Maintenance", "Laundry"]

def trigger_voice(command_key):
    mapping = {
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "win": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3"
    }
    file = mapping.get(command_key, random.choice(["are-you-cooperating.mp3", "are-you-kidding-me.mp3", "i-gotta-pick-somebody.mp3"]))
    if os.path.exists(file): st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 5. PROGRESS & STREAK LOGIC ---
total_tasks = len(defaults) + len(st.session_state.custom_tasks)
completed_count = len(st.session_state.completed_defaults) + sum(1 for t in st.session_state.custom_tasks if t['done'])
progress_val = completed_count / total_tasks if total_tasks > 0 else 0

if progress_val == 1.0 and st.session_state.last_completion_date != today_date:
    if st.session_state.last_completion_date == today_date - datetime.timedelta(days=1):
        st.session_state.streak += 1
    else: st.session_state.streak = 1
    st.session_state.last_completion_date = today_date
    if st.session_state.streak > st.session_state.best_streak: st.session_state.best_streak = st.session_state.streak
    st.balloons()
    trigger_voice("win")

# --- 6. UI HEADER ---
st.title("🏏 THE SANCTUARY")
st.markdown(f'<div class="streak-box"><h2 style="margin:0; color:#ff4b4b;">🔥 STREAK: {st.session_state.streak} DAYS</h2></div>', unsafe_allow_html=True)
st.write(f"### PROGRESS: {int(progress_val * 100)}%")
st.progress(progress_val)

# --- 7. MISSION LOG ---
st.write("### 📜 FIELD ORDERS")
new_task = st.text_input("Manual Entry:", placeholder="Add a custom task...", label_visibility="collapsed")
if st.button("➕ ADD TASK"):
    if new_task:
        st.session_state.custom_tasks.append({"name": new_task, "done": False})
        trigger_voice("question")
        st.rerun()

st.write("---")
for t in defaults:
    if t not in st.session_state.completed_defaults:
        if st.button(f"✔️ {t}", key=f"def_{t}"):
            st.session_state.points += 20
            st.session_state.completed_defaults.append(t)
            st.rerun()
    else: st.button(f"✅ {t} (SECURED)", key=f"done_{t}", disabled=True)

for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ {ct['name']}", key=f"cust_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30
            st.rerun()
    else: st.button(f"🌟 {ct['name']} (SECURED)", key=f"cdone_{i}", disabled=True)

# --- 8. VAULT & SPECIAL BONUS (SIDEBAR) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
st.sidebar.write(f"🏆 Best: {st.session_state.best_streak} Days")
st.sidebar.write("---")

# SPECIAL 7-DAY BONUS LOGIC
st.sidebar.subheader("💀 SPECIAL BONUSES")
if st.session_state.streak >= 7:
    st.sidebar.markdown('<div class="bonus-unlocked">🔓 7-DAY CHALLENGE COMPLETE</div>', unsafe_allow_html=True)
    if st.sidebar.button("🎁 CLAIM: MASTER SAVIOR REWARD"):
        st.session_state.points += 500
        st.sidebar.balloons()
        st.sidebar.success("500 BONUS POINTS ADDED!")
else:
    st.sidebar.markdown(f'<div class="bonus-locked">🔒 LOCKED: Reach a 7-day streak to unlock the Warlord Bonus (Current: {st.session_state.streak}/7)</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("🎁 REWARDS")
rewards = [("☕ Coffee", 20), ("🍺 Cider", 40), ("🦶 Massage", 80), ("🛍️ Shopping", 300)]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.rerun()

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.completed_defaults = []
    st.session_state.custom_tasks = []
    st.rerun()
