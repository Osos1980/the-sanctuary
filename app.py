import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")
SAVE_FILE = "sanctuary_save.json"

# --- STYLE ---
st.markdown("""
<style>
.main { background-color: #0e1117; color: white; }
.stButton>button {
    width: 100%; height: 60px;
    font-size: 18px; border-radius: 15px;
    background-color: #ff4b4b; color: white;
    font-weight: bold;
}
.negan-box {
    background:#1e2129;
    padding:15px;
    border-left:6px solid #ff4b4b;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            return json.load(open(SAVE_FILE))
        except:
            return {}
    return {}

def save_data():
    safe = {k: v for k, v in st.session_state.items()
            if isinstance(v, (int, float, str, list, dict, bool))}
    json.dump(safe, open(SAVE_FILE, "w"))

data = load_data()

def init(k, v):
    if k not in st.session_state:
        st.session_state[k] = data.get(k, v)

# --- STATE ---
init("points", 100)
init("xp", 0)
init("level", 1)
init("completed_tasks", [])
init("manual_tasks", [])
init("boss_hp", 100)
init("last_day", "")
init("last_msg", "Waiting on you, Jessica.")
init("combo", 0)
init("last_task_time", time.time())
init("negan_mood", 0)
init("last_interrupt", 0)
init("weekly", [0]*7)

# --- TIME ---
central = pytz.timezone('US/Central')
now = datetime.datetime.now(central)
today = str(now.date())
weekday = now.weekday()

# --- DAILY RESET ---
if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    st.session_state.last_msg = random.choice([
        "Rise and shine.",
        "Let's get to work.",
        "New day. My rules."
    ])
    save_data()

# --- VOICE ---
def negan_speak(text):
    st.session_state.last_msg = text
    st.toast(text)

    st.markdown(f"""
    <script>
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.rate = 0.85;
    msg.pitch = 0.6;
    speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🏏 THE SANCTUARY")

col1, col2 = st.columns([1,3])

with col1:
    if os.path.exists("negan.png"):
        st.image("negan.png", use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="negan-box">
    🧟 "{st.session_state.last_msg}"
    </div>
    """, unsafe_allow_html=True)

# --- INTERRUPT SYSTEM ---
now_time = time.time()
if now_time - st.session_state.last_interrupt > random.randint(180,300):
    st.session_state.last_interrupt = now_time
    msg = random.choice([
        "Do one task. Now.",
        "Move.",
        "Stop stalling.",
        "2 minutes. Go."
    ])
    st.error(f"⚠️ {msg}")
    negan_speak(msg)

# --- STATS ---
c1, c2, c3 = st.columns(3)
c1.metric("LEVEL", st.session_state.level)
c2.metric("POINTS", st.session_state.points)
c3.metric("BOSS", f"{st.session_state.boss_hp}%")

st.progress(st.session_state.xp / 100)

# --- MISSIONS ---
st.write("## 🎯 MISSIONS")

presets = ["Coffee", "Clean", "Laundry", "Reset"]
tasks = presets + st.session_state.manual_tasks

for t in tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):

            now_time = time.time()
            if now_time - st.session_state.last_task_time < 120:
                st.session_state.combo += 1
            else:
                st.session_state.combo = 1

            st.session_state.last_task_time = now_time

            bonus = st.session_state.combo * 5

            st.session_state.completed_tasks.append(t)
            st.session_state.points += 25 + bonus
            st.session_state.xp += 20 + bonus
            st.session_state.weekly[weekday] += 1

            if st.session_state.combo >= 3:
                negan_speak("That's momentum.")
            else:
                negan_speak("Good.")

            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up.")

            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t}", disabled=True, key=f"d{t}")

# --- FOCUS ---
st.write("## ⏱️ FOCUS")

if st.button("2 MIN"):
    st.session_state.timer = time.time()
    st.session_state.timer_len = 120

if st.button("5 MIN"):
    st.session_state.timer = time.time()
    st.session_state.timer_len = 300

if "timer" in st.session_state:
    remain = max(0, st.session_state.timer_len - int(time.time() - st.session_state.timer))
    st.write(remain)
    if remain == 0:
        st.session_state.xp += 30
        negan_speak("Focus complete.")
        del st.session_state.timer

# --- GAMES ---
st.write("## 🎮")

if st.button("⚔️ ATTACK"):
    dmg = random.randint(20,40)
    st.session_state.boss_hp -= dmg
    if dmg > 35:
        st.success(f"CRITICAL {dmg}")
    else:
        st.info(dmg)

    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 100
        st.balloons()
        negan_speak("Boss down.")

if st.button("🔦 SCAVENGE"):
    if st.session_state.points >= 20:
        st.session_state.points -= 20
        if random.random() > 0.5:
            win = random.randint(40,80)
            st.session_state.points += win
            negan_speak("Jackpot.")
        else:
            negan_speak("Nothing.")

# --- INTERRUPT BUTTON ---
if st.button("🧠 SNAP ME OUT OF IT"):
    msg = random.choice(["Do one task", "Move", "Drink water"])
    st.error(msg)
    negan_speak(msg)

# --- WEEKLY ---
st.write("## 📊 WEEKLY")
cols = st.columns(7)
for i, v in enumerate(st.session_state.weekly):
    cols[i].metric(str(i+1), v)

# --- SIDEBAR ---
st.sidebar.metric("Points", st.session_state.points)

if st.sidebar.button("RESET"):
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
