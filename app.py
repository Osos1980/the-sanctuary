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
        width: 100%; height: 65px; font-size: 18px; 
        border-radius: 20px; background-color: #ff4b4b; 
        color: white; font-weight: bold; border: none;
    }
    .stProgress > div > div > div > div { background-color: #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    .stats-box { background: #1e2129; padding: 15px; border-radius: 15px; border: 1px solid #333; margin-bottom: 15px; text-align: center; }
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
init("completed_tasks", [])
init("performance_score", 0)
init("trend", 0.0)
init("boss_hp", 100)
init("last_action", time.time())
init("burnout", 0)
init("weekly", [0]*7)
init("last_voice", "")
init("last_mood_msg", "") # NEW: Tracks state change for mood
init("last_idle_penalty", 0)
init("last_day", "")
init("last_week", 0)
init("last_burnout_tick", 0)

# --- 3. TIME & RESETS ---
central = pytz.timezone('US/Central')
now = datetime.datetime.now(central)
today = str(now.date())
weekday = now.weekday()
week_num = now.isocalendar()[1]

if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today

if st.session_state.last_week != week_num:
    st.session_state.weekly = [0]*7
    st.session_state.last_week = week_num

# --- 4. NEGAN VOICE (STATE SENSITIVE) ---
def negan_speak(text):
    # Prevents double-triggering on the same render
    st.markdown(f"""<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance("{text}");
    msg.rate = 0.85; msg.pitch = 0.6; window.speechSynthesis.speak(msg);</script>""", unsafe_allow_html=True)

# --- 5. CORE LOGIC ---
st.session_state.trend *= 0.98
score = st.session_state.performance_score
trend = st.session_state.trend

# Difficulty logic
if score > 6: task_limit = 5
elif score < -3: task_limit = 2
else: task_limit = 4

# --- 6. HEADER & MOOD LOGIC (STATE CHANGE ONLY) ---
st.title("🏏 THE SANCTUARY")

if trend > 5: msg = "You've been consistent. I like that."
elif trend < -5: msg = "This pattern isn't working for me."
elif score > 6: msg = "Now THAT is what I like to see."
elif score < -4: msg = "You're slipping, Jessica."
else: msg = "Don't disappoint me today."

# 🔥 FIX 1: Only speak if the mood message has actually changed
if msg != st.session_state.last_mood_msg:
    negan_speak(msg)
    st.session_state.last_mood_msg = msg

st.markdown(f'<div class="stats-box">🧟 {msg}</div>', unsafe_allow_html=True)

st.write(f"**LEVEL {st.session_state.level}**")
st.progress(st.session_state.xp / 100)

# --- 7. MISSIONS ---
all_tasks = ["Coffee recharge", "Clean Zone", "Laundry", "Organize", "Reset Space"]
tasks = all_tasks[:task_limit]

st.write("## 🎯 MISSIONS")
for t in tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            reward = 10 if score < 0 else 30 if score > 5 else 20
            st.session_state.completed_tasks.append(t)
            st.session_state.points += reward
            st.session_state.performance_score += 1
            st.session_state.trend += 1.5
            st.session_state.weekly[weekday] += 1
            st.session_state.xp += 25
            
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                negan_speak("Level up. You're moving up.")
            
            st.session_state.last_action = time.time()
            negan_speak("Good. Keep going.")
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t}", disabled=True)

# --- 8. BOSS BATTLE (ENHANCED FEEDBACK) ---
st.write("---")
st.write("🧟 **BOSS HP**")
st.progress(st.session_state.boss_hp / 100)

# 🔥 FIX 2: Emotional reinforcement on Attack
if st.button("⚔️ ATTACK"):
    dmg = random.randint(20, 40)
    st.session_state.boss_hp -= dmg
    
    if dmg > 35:
        st.success(f"💥 CRITICAL HIT {dmg}")
        negan_speak("Now that's how it's done.")
    else:
        st.info(f"Hit for {dmg}")
    
    if st.session_state.boss_hp <= 0:
        st.session_state.boss_hp = 100
        st.session_state.points += 100
        st.balloons()
        negan_speak("Boss down. Easy peasy.")
    
    save_data()

# --- 9. IDLE, BURNOUT & QUICK ACTION ---
idle = time.time() - st.session_state.last_action
if idle > 300 and time.time() - st.session_state.last_idle_penalty > 300:
    st.warning("⚠️ Negan is staring... focus.")
    st.session_state.performance_score -= 1
    st.session_state.trend -= 1
    st.session_state.last_idle_penalty = time.time()
    negan_speak("Focus.")

if score > 8 and time.time() - st.session_state.last_burnout_tick > 120:
    st.session_state.burnout += 1
    st.session_state.last_burnout_tick = time.time()

if st.session_state.burnout >= 3:
    st.error("🚨 Break required.")
    if st.button("START BREAK"):
        st.session_state.break_start = time.time()

if "break_start" in st.session_state:
    remain = max(0, 300 - int(time.time() - st.session_state.break_start))
    st.write(f"Recovery: {remain}s")
    if remain == 0:
        st.session_state.burnout = 0
        st.session_state.performance_score = 4
        del st.session_state.break_start
        negan_speak("Back to work.")
        save_data()

if st.button("🧠 WHAT NOW?"):
    action = random.choice(["Do one task", "Drink water", "2 min movement"])
    st.info(action)
    negan_speak(action)

# --- 10. WEEKLY PROGRESS ---
st.write("---")
st.write("## 📊 WEEKLY PROGRESS")
days = ["M","T","W","T","F","S","S"]
cols = st.columns(7)
for i, val in enumerate(st.session_state.weekly):
    cols[i].metric(days[i], val)
    cols[i].progress(min(val/5, 1.0) if val > 0 else 0.0)

st.sidebar.title("💎 VAULT")
st.sidebar.metric("Points", st.session_state.points)
if st.sidebar.button("💀 FULL RESET"):
    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()
