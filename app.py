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
    .quote-box { padding: 15px; border-left: 5px solid #ff4b4b; background-color: #1e2129; font-style: italic; margin-bottom: 20px; border-radius: 0 10px 10px 0; color: #eee; }
    .bonus-locked { color: #555; font-style: italic; text-align: center; font-size: 0.9em; border: 1px dashed #444; padding: 10px; border-radius: 10px; }
    .bonus-unlocked { color: #00ff00; font-weight: bold; text-align: center; border: 2px solid #00ff00; padding: 10px; border-radius: 10px; background: #002200; }
    .hof-item { color: #ffd700; font-weight: bold; text-align: center; border: 1px goldenrod solid; border-radius: 10px; padding: 5px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CENTRAL TIME & GREETING LOGIC ---
central = pytz.timezone('US/Central')
now_central = datetime.datetime.now(central)
today_date = now_central.date()
current_hour = now_central.hour
current_day = now_central.strftime("%A")

def get_greeting(hour):
    if hour < 12: return "Good Morning, Jessica. The sun is up, and so is the tax. Time to earn your keep."
    elif 12 <= hour < 18: return "Good Afternoon, Jessica. Halfway there. Don't let the momentum slide."
    else: return "Good Evening, Jessica. The perimeter is holding. Finish strong."

negan_quotes = [
    "I appreciate you, Jessica. Now get back to work.",
    "People are counting on you. Take it like a champ.",
    "Documentation is the law of the land. Don't break it, Jess.",
    "Easy peasy lemon squeezy. Just get it done.",
    "You're the boss of this house. Act like it.",
    "I hope you have your shitting pants on, because we’ve got work to do.",
    "Starving, working, bleeding... that is how you build a life.",
    "You earn what you take, and you keep what you can hold."
]

# --- 3. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "custom_tasks" not in st.session_state: st.session_state.custom_tasks = []
if "completed_defaults" not in st.session_state: st.session_state.completed_defaults = []
if "streak" not in st.session_state: st.session_state.streak = 0
if "best_streak" not in st.session_state: st.session_state.best_streak = 0
if "last_completion_date" not in st.session_state: st.session_state.last_completion_date = None

# --- 4. AUDIO ENGINE ---
negan_playlist = [
    "all-you-gotta-do-is-answer-one-simple-question.mp3",
    "are-you-cooperating.mp3",
    "are-you-kidding-me.mp3",
    "do-not-let-me-distract-you-young-man.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
    "i-think-it-would-be-enjoyable-screw-your-brains-out.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
]

def trigger_voice(command_key="random"):
    mapping = {
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "win": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        with open(file, 'rb') as f:
            st.audio(f.read(), format='audio/mp3')
    else:
        st.sidebar.warning(f"Audio file missing: {file}")

# --- 5. PROGRESS & STREAK LOGIC ---
is_work = current_day in ["Friday", "Saturday", "Sunday"]
defaults = ["Handover & Meds", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee Recharge", "Groceries", "Base Maintenance", "Laundry"]

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
st.write(f"### MISSION PROGRESS: {int(progress_val * 100)}%")
st.progress(progress_val)

st.write(f"### {get_greeting(current_hour)}")
st.markdown(f'<div class="quote-box">"{random.choice(negan_quotes)}"</div>', unsafe_allow_html=True)

# --- 7. FIELD ORDERS (MANUAL TASKS) ---
st.write("### 📜 NEW FIELD ORDERS")
new_task = st.text_input("Manual Entry:", placeholder="Add something custom...", label_visibility="collapsed")
if st.button("➕ ADD TO LOG"):
    if new_task:
        st.session_state.custom_tasks.append({"name": new_task, "done": False})
        trigger_voice("question")
        st.rerun()

# --- 8. MISSION LOG ---
st.write("---")
st.write(f"### 🎯 {'HOSPITAL' if is_work else 'HOME BASE'} OBJECTIVES")

for t in defaults:
    if t not in st.session_state.completed_defaults:
        if st.button(f"✔️ {t}", key=f"def_{t}"):
            st.session_state.points += 20
            st.session_state.completed_defaults.append(t)
            trigger_voice("random")
            st.rerun()
    else: st.button(f"✅ {t} (SECURED)", key=f"done_{t}", disabled=True)

for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ CUSTOM: {ct['name']}", key=f"cust_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30
            trigger_voice("win")
            st.rerun()
    else: st.button(f"🌟 {ct['name']} (SECURED)", key=f"cdone_{i}", disabled=True)

# --- 9. VAULT, HOF & SPECIAL BONUS (SIDEBAR) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
st.sidebar.write("---")

st.sidebar.subheader("🏆 HALL OF FAME")
st.sidebar.markdown(f'<div class="hof-item">👑 BEST STREAK: {st.session_state.best_streak} DAYS</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("💀 SPECIAL BONUS")
if st.session_state.streak >= 7:
    st.sidebar.markdown('<div class="bonus-unlocked">🔓 7-DAY CHALLENGE COMPLETE</div>', unsafe_allow_html=True)
    if st.sidebar.button("🎁 CLAIM 500 PTS"):
        st.session_state.points += 500
        st.sidebar.balloons()
        st.rerun()
else:
    st.sidebar.markdown(f'<div class="bonus-locked">🔒 LOCKED: {st.session_state.streak}/7 Days</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("🎁 REWARDS")
rewards = [("☕ Coffee", 20), ("🍺 Cider", 40), ("🦶 Massage", 80), ("🍽️ Dinner", 150), ("🛍️ Shopping", 300)]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.success(f"Claimed {name}!")
            st.rerun()

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.completed_defaults = []
    st.session_state.custom_tasks = []
    st.rerun()
