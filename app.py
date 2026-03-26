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

# --- 2. JESSICA'S PERSONAL QUOTE LIBRARY ---
# These are the specific "Voices" you were looking for.
MORNING_GREETINGS = [
    "Wakey wakey, Jessica. Eggs and bakey... Lucille is hungry for some productivity.",
    "Look at you, Jessica. Still breathing. Let's make it count today.",
    "I am everywhere, Jessica. Especially in your to-do list. Get to it.",
    "Today is a brand new day in the Sanctuary. Don't disappoint me."
]

DAY_ENCOURAGEMENT = [
    "You're killing it, Jessica. Keep that momentum.",
    "I'm starting to think you've got guts, Jessica. Real guts.",
    "Look at you go. Efficient. Cold. Productive.",
    "That's how a Saviour does it. Good job."
]

IDLE_WARNINGS = [
    "Tick tock, Jessica. I don't like being bored.",
    "Are we having a little nap? Because I'm wide awake.",
    "You're drifting, Jessica. Focus. Now."
]

# --- 3. PERSISTENCE & INIT ---
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
init("last_voice_msg", "Standing by...")

# --- 4. THE UPDATED VOICE ENGINE ---
def negan_speak(text):
    st.session_state.last_voice_msg = text
    # 1. Visual Backup (In case sound is blocked)
    st.toast(f"🧟 {text}") 
    
    # 2. Browser Audio Script
    st.markdown(f"""
    <script>
    window.speechSynthesis.cancel(); // Clear queue
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 0.8; 
    msg.pitch = 0.5;
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# --- 5. DAILY GREETING LOGIC ---
central = pytz.timezone('US/Central')
today = str(datetime.datetime.now(central).date())

# If Jessica opens the app and it's a new day:
if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    greeting = random.choice(MORNING_GREETINGS)
    negan_speak(greeting) # Trigger Morning Voice
    save_data()

# --- 6. INTERFACE ---
st.title("🏏 THE SANCTUARY")

# THE VISUAL GREETING (Always visible)
st.info(f"🧟 **NEGAN'S MESSAGE:** {st.session_state.last_voice_msg}")

c1, c2, c3 = st.columns(3)
c1.metric("LEVEL", st.session_state.level)
c2.metric("XP", f"{st.session_state.xp}/100")
c3.metric("POINTS", st.session_state.points)

# --- 7. MANUAL MISSION ADDER ---
st.write("### ➕ ADD CUSTOM MISSION")
with st.form("add_task", clear_on_submit=True):
    new_task = st.text_input("What's the play, Jessica?")
    if st.form_submit_button("ADD TO LOG"):
        if new_task:
            st.session_state.manual_tasks.append(new_task)
            negan_speak(f"Adding {new_task}. Do it right.")
            save_data()
            st.rerun()

# --- 8. MISSION LOG ---
st.write("### 🎯 ACTIVE MISSIONS")
base_tasks = ["Coffee recharge", "Clean Base", "Laundry", "Organize"]
all_tasks = base_tasks + st.session_state.manual_tasks

for t in all_tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            st.session_state.completed_tasks.append(t)
            st.session_state.xp += 25
            st.session_state.points += 20
            
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up, Jessica. You're becoming a legend.")
            else:
                negan_speak(random.choice(DAY_ENCOURAGEMENT))
            
            st.session_state.last_action = time.time()
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}")

# --- 9. BOSS FIGHT ---
st.write("---")
st.write(f"🧟 **BOSS HEALTH: {st.session_state.boss_hp}%**")
if st.button("⚔️ ATTACK BOSS"):
    dmg = random.randint(20, 45)
    st.session_state.boss_hp -= dmg
    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 100
        st.balloons()
        negan_speak("Boss down. Not bad, Jessica. Not bad at all.")
    else:
        negan_speak(f"Hit for {dmg}!")
    save_data()

# --- 10. VOICE FIX & RESET ---
st.sidebar.title("⚙️ COMMANDS")
if st.sidebar.button("🔊 UNMUTE/HEAR NEGAN"):
    negan_speak(st.session_state.last_voice_msg)

if st.sidebar.button("💀 FULL RESET"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
