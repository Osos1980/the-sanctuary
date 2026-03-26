import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")
SAVE_FILE = "sanctuary_save.json"

# --- 2. THE NEGAN REPERTOIRE (GREETINGS & VOICES) ---
# These are the actual lines Negan will use for Jessica
GREETINGS = [
    "Wakey wakey, Jessica. Eggs and bakey.",
    "Look at you, Jessica. Still breathing. Get to work.",
    "I am everywhere, Jessica. Don't make me wait.",
    "Today is the day we get things done. My way."
]

PRAISE = [
    "Hot diggity dog! One down.",
    "See? That wasn't so hard, was it, Jessica?",
    "That’s how a professional does it.",
    "Simple. Efficient. I like it."
]

THREATS = [
    "You're slipping, Jessica. I'm losing my patience.",
    "Tick tock. I don't like being bored.",
    "Are we having a little nap? Lucille is wide awake."
]

# --- 3. PERSISTENCE ---
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

# --- 4. INITIALIZATION ---
def init(k, v):
    if k not in st.session_state: st.session_state[k] = data.get(k, v)

init("points", 0)
init("xp", 0)
init("level", 1)
init("completed_tasks", [])
init("manual_tasks", [])
init("boss_hp", 100)
init("last_action", time.time())
init("last_day", "")
init("last_mood_msg", "Standing by, Jessica...")

# --- 5. THE VOICE ENGINE ---
def negan_speak(text):
    st.session_state.last_mood_msg = text
    # This script forces the browser to speak
    st.markdown(f"""
    <script>
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.rate = 0.8; msg.pitch = 0.5;
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# --- 6. DAILY RESET & MORNING GREETING ---
central = pytz.timezone('US/Central')
today = str(datetime.datetime.now(central).date())

if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    # This triggers the Morning Greeting
    startup_line = random.choice(GREETINGS)
    negan_speak(startup_line)
    save_data()

# --- 7. UI LAYOUT ---
st.title("🏏 THE SANCTUARY")

# THE NEGAN BOX (Visualizing the Greetings)
st.error(f"🧟 NEGAN SAYS: {st.session_state.last_mood_msg}")

# Stats Row
c1, c2, c3 = st.columns(3)
c1.metric("LEVEL", st.session_state.level)
c2.metric("POINTS", st.session_state.points)
c3.metric("BOSS HP", f"{st.session_state.boss_hp}%")
st.progress(st.session_state.xp / 100)

# --- 8. MANUAL TASK ADDER ---
st.write("### ➕ ADD CUSTOM MISSION")
with st.form("task_form", clear_on_submit=True):
    custom_task = st.text_input("New objective for Jessica:")
    if st.form_submit_button("ADD TO MISSION LOG"):
        if custom_task:
            st.session_state.manual_tasks.append(custom_task)
            negan_speak(f"Adding {custom_task}. Don't screw it up.")
            save_data()
            st.rerun()

# --- 9. THE MISSION LOG ---
st.write("### 🎯 ACTIVE MISSIONS")
base_tasks = ["Coffee", "Clean", "Laundry", "Organize"]
all_tasks = base_tasks + st.session_state.manual_tasks

for t in all_tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            st.session_state.completed_tasks.append(t)
            st.session_state.points += 20
            st.session_state.xp += 25
            
            # Level Up Logic
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up. You're becoming an asset.")
            else:
                negan_speak(random.choice(PRAISE))
            
            st.session_state.last_action = time.time()
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}")

# --- 10. BOSS ATTACK ---
st.write("---")
if st.button("⚔️ ATTACK BOSS"):
    dmg = random.randint(20, 45)
    st.session_state.boss_hp -= dmg
    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 100
        st.balloons()
        negan_speak("Boss down. Not bad, Jessica.")
    else:
        negan_speak(f"Hit for {dmg}!")
    save_data()

# --- 11. MANUAL VOICE TRIGGER ---
st.sidebar.write("### 🎙️ VOICE CONTROL")
if st.sidebar.button("🔊 HEAR NEGAN"):
    negan_speak(st.session_state.last_mood_msg)

if st.sidebar.button("💀 RESET SYSTEM"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
