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

# --- 2. THE VOICE & QUOTE LIBRARY ---
QUOTES = {
    "morning": [
        "Wakey wakey, Jessica. Eggs and bakey... Lucille is hungry.",
        "Look at you, Jessica. Still breathing. Get to work.",
        "New day, Jessica. New rules. My rules."
    ],
    "praise": [
        "Hot diggity dog! Good job, Jessica.",
        "That’s how a professional does it, Jessica.",
        "Simple. Efficient. I like it."
    ],
    "boss_hit": [
        "Ooh! That had to hurt!",
        "Keep swinging, Jessica! Don't stop now!",
        "You're redlining it! I love it!"
    ]
}

# --- 3. DATA PERSISTENCE ---
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

init("points", 50)
init("xp", 0)
init("level", 1)
init("completed_tasks", [])
init("manual_tasks", [])
init("boss_hp", 100)
init("last_day", "")
init("last_msg", "Awaiting orders, Jessica...")

# --- 4. VOICE ENGINE ---
def negan_speak(text):
    st.session_state.last_msg = text
    st.toast(text)
    st.markdown(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.rate = 0.8; msg.pitch = 0.5;
        window.speechSynthesis.speak(msg);
        </script>
    """, unsafe_allow_html=True)

# --- 5. HEADER & GREETING ---
st.title("🏏 THE SANCTUARY")

# Morning Reset Logic
central = pytz.timezone('US/Central')
today = str(datetime.datetime.now(central).date())
if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    negan_speak(random.choice(QUOTES["morning"]))
    save_data()

# NEGAN BOX
st.info(f"🧟 **NEGAN SAYS:** {st.session_state.last_msg}")

# STATS
col_lvl, col_pts = st.columns(2)
col_lvl.metric("LEVEL", st.session_state.level)
col_pts.metric("POINTS", st.session_state.points)
st.progress(st.session_state.xp / 100, text=f"XP: {st.session_state.xp}/100")

st.write("---")

# --- 6. MISSIONS ---
st.subheader("🎯 JESSICA'S MISSIONS")
# Add Custom Task
with st.expander("➕ ADD NEW MISSION"):
    new_t = st.text_input("New objective:")
    if st.button("CONFIRM"):
        if new_t:
            st.session_state.manual_tasks.append(new_t)
            negan_speak(f"Adding {new_t}. Don't screw it up.")
            save_data()
            st.rerun()

# Mission List
presets = ["Coffee Recharge", "Clean Workspace", "Laundry", "Daily Reset"]
all_t = presets + st.session_state.manual_tasks
for t in all_t:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t, use_container_width=True):
            st.session_state.completed_tasks.append(t)
            st.session_state.points += 25
            st.session_state.xp += 20
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up, Jessica! You're an asset.")
            else:
                negan_speak(random.choice(QUOTES["praise"]))
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}", use_container_width=True)

st.write("---")

# --- 7. THE BOSS BATTLE (FIXED & PROMINENT) ---
st.subheader("🧟 THE BOSS FIGHT")
st.write(f"Boss Health: **{st.session_state.boss_hp}%**")
st.progress(st.session_state.boss_hp / 100)

# THE BIG RED ATTACK BUTTON
if st.button("💥 ATTACK BOSS", type="primary", use_container_width=True):
    damage = random.randint(20, 45)
    st.session_state.boss_hp -= damage
    
    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 150
        st.balloons()
        negan_speak("Boss down! Take the spoils, Jessica!")
    else:
        negan_speak(f"You hit for {damage}! {random.choice(QUOTES['boss_hit'])}")
    
    save_data()
    st.rerun()

st.write("---")

# --- 8. SIDEBAR TOOLS ---
with st.sidebar:
    st.title("🛠️ TOOLS")
    if st.button("🔊 TEST SOUND"):
        negan_speak("Can you hear me now, Jessica?")
    
    st.write("---")
    st.subheader("🎲 SCAVENGE")
    if st.button("🔦 ATTEMPT SCAVENGE (20 pts)"):
        if st.session_state.points >= 20:
            st.session_state.points -= 20
            if random.random() > 0.5:
                gain = random.randint(40, 70)
                st.session_state.points += gain
                negan_speak(f"Nice find! You got {gain} points.")
            else:
                negan_speak("Nothing there but dust.")
            save_data()
            st.rerun()
    
    if st.button("💀 RESET ALL"):
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()
