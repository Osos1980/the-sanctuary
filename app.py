import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- 1. CONFIG & STYLING ---
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
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    .negan-box { 
        background-color: #1e2129; padding: 20px; 
        border-left: 10px solid #ff4b4b; border-radius: 10px; 
        margin-bottom: 25px;
    }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE VOICE & QUOTE REPERTOIRE ---
QUOTES = {
    "morning": [
        "Wakey wakey, Jessica. Eggs and bakey... Lucille is hungry.",
        "Look at you, Jessica. Still breathing. Get to work.",
        "New day, Jessica. New rules. My rules.",
        "The Sanctuary doesn't run itself, Jessica. Move it!"
    ],
    "praise": [
        "Hot diggity dog! Good job, Jessica.",
        "That’s how a professional does it, Jessica.",
        "I’m starting to think you’ve got guts.",
        "Simple. Efficient. I like it."
    ],
    "games": [
        "You're gambling with my resources, Jessica? Bold.",
        "Easy pickings out there today.",
        "Winning is a habit, Jessica. Don't break it."
    ]
}

# --- 3. DATA CORE ---
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

init("points", 100)
init("xp", 0)
init("level", 1)
init("completed_tasks", [])
init("manual_tasks", [])
init("boss_hp", 100)
init("last_day", "")
init("last_msg", "Awaiting authorization, Jessica...")

# --- 4. THE VOICE ENGINE ---
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

# --- 5. MORNING INITIALIZATION ---
central = pytz.timezone('US/Central')
today = str(datetime.datetime.now(central).date())

if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    # Auto-pick morning greeting
    st.session_state.last_msg = random.choice(QUOTES["morning"])
    save_data()

# --- 6. HEADER & NEGAN VISUAL ---
st.title("🏏 THE SANCTUARY")

st.markdown(f"""
    <div class="negan-box">
        <h3 style="margin:0; font-size:16px;">🧟 NEGAN SAYS:</h3>
        <p style="font-size:22px; font-style:italic; margin-top:10px;">"{st.session_state.last_msg}"</p>
    </div>
""", unsafe_allow_html=True)

# STATS BAR
c1, c2, c3 = st.columns(3)
c1.metric("LEVEL", st.session_state.level)
c2.metric("POINTS", st.session_state.points)
c3.metric("BOSS HP", f"{st.session_state.boss_hp}%")
st.progress(st.session_state.xp / 100, text=f"XP: {st.session_state.xp}/100")

# --- 7. MISSIONS (CORE FEATURE) ---
st.write("## 🎯 MISSIONS")
with st.expander("➕ ADD CUSTOM MISSION"):
    new_t = st.text_input("Assign a new task for Jessica:")
    if st.button("CONFIRM TASK"):
        if new_t:
            st.session_state.manual_tasks.append(new_t)
            negan_speak(f"Adding {new_t}. Don't screw it up.")
            save_data()
            st.rerun()

presets = ["Coffee Recharge", "Clean Workspace", "Laundry", "Daily Reset"]
all_tasks = presets + st.session_state.manual_tasks

for t in all_tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            st.session_state.completed_tasks.append(t)
            st.session_state.points += 25
            st.session_state.xp += 20
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up, Jessica! You're becoming an asset.")
            else:
                negan_speak(random.choice(QUOTES["praise"]))
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t} (SECURED)", disabled=True, key=f"done_{t}")

st.write("---")

# --- 8. THE GAMES (3 FEATURES) ---
st.write("## 🎮 THE GAMES")

tab1, tab2, tab3 = st.tabs(["🧟 BOSS FIGHT", "🔦 SCAVENGE", "🎲 SUPPLY RUN"])

with tab1:
    st.write("### ATTACK THE BOSS")
    st.progress(st.session_state.boss_hp / 100)
    if st.button("💥 STRIKE WITH LUCILLE", type="primary"):
        dmg = random.randint(20, 45)
        st.session_state.boss_hp -= dmg
        if st.session_state.boss_hp <= 0:
            st.session_state.boss_hp = 100
            st.session_state.points += 150
            st.balloons()
            negan_speak("Boss down! Take the spoils, Jessica.")
        else:
            negan_speak(f"You hit for {dmg} damage!")
        save_data()
        st.rerun()

with tab2:
    st.write("### SCAVENGE FOR LOOT")
    st.write("Costs 20 Points. Risk it all?")
    if st.button("🔦 ENTER THE DARK"):
        if st.session_state.points >= 20:
            st.session_state.points -= 20
            roll = random.random()
            if roll > 0.5:
                win = random.randint(40, 80)
                st.session_state.points += win
                negan_speak(f"Jackpot! You found {win} points.")
            else:
                negan_speak("Nothing but walkers out there. Waste of time.")
            save_data()
            st.rerun()
        else:
            st.warning("Not enough points, Jessica.")

with tab3:
    st.write("### SUPPLY RUN (LUCK DRAW)")
    st.write("Free daily draw. Win XP or Points!")
    if st.button("🎲 PULL THE TRIGGER"):
        outcome = random.choice(["+10 XP", "+20 Points", "No Luck", "+50 Points!"])
        if "+10 XP" in outcome: st.session_state.xp = min(100, st.session_state.xp + 10)
        if "Points" in outcome: 
            val = 20 if "20" in outcome else 50
            st.session_state.points += val
        negan_speak(f"Supply Run result: {outcome}")
        save_data()
        st.rerun()

# --- 9. SIDEBAR & MAINTENANCE ---
with st.sidebar:
    st.title("🛠️ COMMANDS")
    if st.button("🔊 ACTIVATE VOICE / RE-GREET"):
        negan_speak(st.session_state.last_msg)
    
    st.write("---")
    if st.button("💀 DELETE ALL DATA"):
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()

    st.write(f"**Current Day:** {today}")
    st.write("**Survivor:** Jessica")
