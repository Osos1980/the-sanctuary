import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- 1. CONFIG & PERSISTENCE ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")
SAVE_FILE = "sanctuary_save.json"

st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; height: 60px; font-size: 18px; 
        border-radius: 15px; background-color: #ff4b4b; 
        color: white; font-weight: bold; border: none;
    }
    .stTextInput>div>div>input { background-color: #1e2129; color: white; border: 1px solid #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; text-transform: uppercase; }
    .negan-card { background: #1e2129; padding: 20px; border-radius: 15px; border-left: 8px solid #ff4b4b; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data():
    safe_data = {k: v for k, v in st.session_state.items() if isinstance(v, (int, float, str, list, dict, bool))}
    with open(SAVE_FILE, "w") as f: json.dump(safe_data, f)

data = load_data()

# --- 2. INITIALIZATION ---
def init(k, v):
    if k not in st.session_state: st.session_state[k] = data.get(k, v)

init("points", 0)
init("xp", 0)
init("level", 1)
init("completed_tasks", []) # Tracks tasks done TODAY
init("manual_tasks", [])    # Tracks Jessica's custom entries
init("performance_score", 0)
init("trend", 0.0)
init("boss_hp", 100)
init("last_action", time.time())
init("last_mood_msg", "")
init("last_day", "")

# --- 3. THE NEGAN DICTIONARY ---
GREETINGS = [
    "Wakey wakey, Jessica. Eggs and bakey... hope you're ready to work.",
    "Look at you, Jessica. Still breathing. Let's keep it that way. Get to it.",
    "I am everywhere, Jessica. Especially here. Don't make me wait.",
    "Today is the day we get things done. My way. The only way."
]

TASK_PRAISE = [
    "Hot diggity dog! One down.",
    "See? That wasn't so hard, was it?",
    "That’s how a professional does it. Good job, Jessica.",
    "Simple. Efficient. I like it."
]

IDLE_THREATS = [
    "You're slipping, Jessica. I'm starting to lose my patience.",
    "Tick tock. I don't like being bored. Do something.",
    "Are we having a little nap? Because Lucille is wide awake."
]

# --- 4. VOICE ENGINE ---
def negan_speak(text):
    st.markdown(f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance("{text}");
    msg.rate = 0.85; msg.pitch = 0.5; window.speechSynthesis.speak(msg);</script>""", unsafe_allow_html=True)

# --- 5. TIME & DAILY RESET ---
central = pytz.timezone('US/Central')
now = datetime.datetime.now(central)
today = str(now.date())

if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    # New Day Greeting
    startup_msg = random.choice(GREETINGS)
    negan_speak(startup_msg)
    st.session_state.last_mood_msg = startup_msg

# --- 6. INTERFACE ---
st.title("🏏 THE SANCTUARY")

# Current Mood/Greeting Display
st.markdown(f'<div class="negan-card">🧟 {st.session_state.last_mood_msg}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("LEVEL", st.session_state.level)
col2.metric("POINTS", st.session_state.points)
st.progress(st.session_state.xp / 100)

# --- 7. MANUAL TASK ENTRY ---
st.write("### ➕ ASSIGN NEW MISSION")
new_t = st.text_input("What needs doing, Jessica?", placeholder="Enter a custom task...")
if st.button("ADD TO LOG"):
    if new_t and new_t not in st.session_state.manual_tasks:
        st.session_state.manual_tasks.append(new_t)
        negan_speak(f"Adding {new_t} to the list. Don't screw it up.")
        save_data()
        st.rerun()

# --- 8. MISSION LOG ---
st.write("### 🎯 MISSION LOG")
# Combine preset tasks with manual tasks
presets = ["Coffee Recharge", "Clean Zone", "Laundry", "Reset Space"]
all_current = presets + st.session_state.manual_tasks

for t in all_current:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=f"btn_{t}"):
            st.session_state.completed_tasks.append(t)
            st.session_state.points += 25
            st.session_state.xp += 20
            st.session_state.last_action = time.time()
            
            # Level Up
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up. You're becoming an asset, Jessica.")
            else:
                negan_speak(random.choice(TASK_PRAISE))
            
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}")

# --- 9. BOSS BATTLE ---
st.write("---")
st.write("🧟 **BOSS HEALTH**")
st.progress(st.session_state.boss_hp / 100)
if st.button("⚔️ ATTACK BOSS"):
    dmg = random.randint(20, 45)
    st.session_state.boss_hp -= dmg
    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 100
        st.balloons()
        negan_speak("Boss down. Easy peasy.")
    else:
        negan_speak("Keep swinging!")
    save_data()

# --- 10. IDLE CHECK ---
idle_time = time.time() - st.session_state.last_action
if idle_time > 600: # 10 minutes
    if random.random() < 0.05: # Rare chance to trigger warning
        negan_speak(random.choice(IDLE_THREATS))

# SIDEBAR RESET
if st.sidebar.button("💀 DELETE ALL PROGRESS"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
