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

# --- 2. JESSICA'S PERSONAL VOICE COMMANDS ---
MORNING_QUOTES = [
    "Wakey wakey, Jessica. Eggs and bakey... Lucille is hungry.",
    "Look at you, Jessica. Still breathing. Get to work.",
    "I am everywhere, Jessica. Don't make me wait.",
    "New day, Jessica. New rules. My rules."
]

FINISH_QUOTES = [
    "Hot diggity dog! Good job, Jessica.",
    "See? That wasn't so hard, was it?",
    "That’s how a professional does it, Jessica.",
    "Simple. Efficient. I like it."
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
init("last_day", "")
init("last_voice_msg", "Awaiting authorization, Jessica...")

# --- 5. THE VOICE ENGINE (FORCED SCRIPT) ---
def negan_speak(text):
    st.session_state.last_voice_msg = text
    # This is a 'Toast' popup so you SEE it instantly
    st.toast(f"🧟 {text}") 
    # This is the JS that triggers the browser voice
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = 'en-US';
    msg.rate = 0.8; 
    msg.pitch = 0.5;
    window.speechSynthesis.cancel(); 
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# --- 6. INTERFACE & "WAKE UP" BUTTON ---
st.title("🏏 THE SANCTUARY")

# --- THE FIX: MANDATORY START BUTTON ---
# Browsers REQUIRE a click to allow sound.
if st.button("🔊 ACTIVATE NEGAN / START DAY"):
    central = pytz.timezone('US/Central')
    today = str(datetime.datetime.now(central).date())
    
    if st.session_state.last_day != today:
        st.session_state.completed_tasks = []
        st.session_state.last_day = today
        line = random.choice(MORNING_QUOTES)
    else:
        line = "I'm already here, Jessica. Get back to work."
    
    negan_speak(line)
    save_data()

# VISUAL FEEDBACK
st.info(f"🧟 **NEGAN'S CURRENT ORDER:** {st.session_state.last_voice_msg}")

col1, col2 = st.columns(2)
col1.metric("LEVEL", st.session_state.level)
col2.metric("POINTS", st.session_state.points)
st.progress(st.session_state.xp / 100)

# --- 7. MANUAL MISSIONS ---
st.write("### ➕ ADD CUSTOM MISSION")
new_t = st.text_input("New objective, Jessica?", key="input")
if st.button("ADD TO LOG"):
    if new_t:
        st.session_state.manual_tasks.append(new_t)
        negan_speak(f"Adding {new_t}. Don't screw it up.")
        save_data()
        st.rerun()

# --- 8. MISSION LOG ---
st.write("### 🎯 ACTIVE MISSIONS")
presets = ["Coffee", "Clean Base", "Laundry", "Organize"]
all_t = presets + st.session_state.manual_tasks

for t in all_t:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            st.session_state.completed_tasks.append(t)
            st.session_state.xp += 25
            st.session_state.points += 20
            
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up, Jessica. You're an asset.")
            else:
                negan_speak(random.choice(FINISH_QUOTES))
            
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True)

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
        negan_speak("Boss down. Easy peasy, Jessica.")
    else:
        negan_speak(f"Hit for {dmg}!")
    save_data()

# SIDEBAR RESET
if st.sidebar.button("💀 DELETE ALL"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
