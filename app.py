import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="wide")
SAVE_FILE = "sanctuary_save.json"

# --- 2. JESSICA'S CUSTOM QUOTES ---
QUOTES = {
    "morning": [
        "Wakey wakey, Jessica. Eggs and bakey... Lucille is hungry.",
        "Look at you, Jessica. Still breathing. Get to work.",
        "New day, Jessica. New rules. My rules.",
        "The Sanctuary doesn't run itself, Jessica. Move it."
    ],
    "praise": [
        "Hot diggity dog! Good job, Jessica.",
        "That’s how a professional does it, Jessica.",
        "I’m starting to think you’ve got guts.",
        "Simple. Efficient. I like it."
    ],
    "game": [
        "Easy pickings out there today, Jessica.",
        "You're gambling with my resources? Bold.",
        "Keep scavenging. We need those supplies."
    ]
}

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
def init(k, v):
    if k not in st.session_state: st.session_state[k] = data.get(k, v)

init("points", 50)
init("xp", 0)
init("level", 1)
init("completed_tasks", [])
init("manual_tasks", [])
init("boss_hp", 100)
init("last_day", "")
init("last_msg", "Ready for orders, Jessica.")

# --- 4. THE VOICE ENGINE (ENHANCED) ---
def negan_speak(text):
    st.session_state.last_msg = text
    # The 'Toast' ensures she sees the greeting even if sound fails
    st.toast(text)
    # Forced JS Voice
    st.markdown(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.rate = 0.8; msg.pitch = 0.5; msg.volume = 1.0;
        window.speechSynthesis.speak(msg);
        </script>
    """, unsafe_allow_html=True)

# --- 5. INTERFACE ---
st.title("🏏 THE SANCTUARY")

# --- NEGAN'S VISUAL COMMAND CENTER ---
st.markdown(f"""
    <div style="background-color:#1e2129; padding:20px; border-left: 10px solid #ff4b4b; border-radius:10px;">
        <h2 style="color:#ff4b4b; margin:0;">🧟 NEGAN SAYS...</h2>
        <p style="font-size:24px; color:white; font-style:italic;">"{st.session_state.last_msg}"</p>
    </div>
""", unsafe_allow_html=True)

# Morning Greeting Logic
central = pytz.timezone('US/Central')
today = str(datetime.datetime.now(central).date())
if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    negan_speak(random.choice(QUOTES["morning"]))
    save_data()

st.write("---")

# Main Dashboard
col_stats, col_missions = st.columns([1, 2])

with col_stats:
    st.subheader("💎 STATUS")
    st.metric("LEVEL", st.session_state.level)
    st.metric("POINTS", st.session_state.points)
    st.write(f"XP: {st.session_state.xp}/100")
    st.progress(st.session_state.xp / 100)
    
    st.write("---")
    # --- THE SCAVENGE GAME ---
    st.subheader("🎲 SCAVENGE GAME")
    st.write("Spend 20 Points to find loot.")
    if st.button("🔦 GO SCAVENGING"):
        if st.session_state.points >= 20:
            st.session_state.points -= 20
            outcome = random.choice(["Found Supplies!", "Ambushed!", "Empty Building"])
            if outcome == "Found Supplies!":
                reward = random.randint(40, 60)
                st.session_state.points += reward
                negan_speak(f"Good find, Jessica! You found {reward} points.")
            elif outcome == "Ambushed!":
                st.session_state.xp = max(0, st.session_state.xp - 10)
                negan_speak("Ambush! You lost some XP, Jessica. Focus!")
            else:
                negan_speak("Nothing but dust. Better luck next time.")
            save_data()
        else:
            st.warning("Not enough points to scavenge.")

with col_missions:
    st.subheader("🎯 JESSICA'S MISSIONS")
    # Add Manual Task
    with st.expander("➕ ADD NEW MISSION"):
        new_t = st.text_input("New objective:")
        if st.button("CONFIRM MISSION"):
            if new_t:
                st.session_state.manual_tasks.append(new_t)
                negan_speak(f"Adding {new_t}. Don't screw it up.")
                save_data()
                st.rerun()

    # Mission Log
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
                    negan_speak("Level up, Jessica. You're an asset.")
                else:
                    negan_speak(random.choice(QUOTES["praise"]))
                save_data()
                st.rerun()
        else:
            st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}", use_container_width=True)

# --- SIDEBAR TOOLS ---
st.sidebar.title("🛠️ TOOLS")
if st.sidebar.button("🔊 TEST SOUND / VOICE"):
    negan_speak("Can you hear me now, Jessica? Lucille is getting impatient.")

if st.sidebar.button("💀 DELETE ALL DATA"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
