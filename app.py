import streamlit as st
import datetime
import random
import os

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #ff3333; box-shadow: 0px 0px 15px #ff4b4b; transform: scale(1.02); }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    .game-box { padding: 15px; border: 1px solid #ff4b4b; border-radius: 15px; background-color: #1e2129; text-align: center; margin-bottom: 10px; }
    .quote-box { padding: 15px; border-left: 5px solid #ff4b4b; background-color: #1e2129; font-style: italic; margin-bottom: 20px; border-radius: 0 10px 10px 0; }
    .stTextInput>div>div>input { background-color: #1e2129; color: white; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "custom_tasks" not in st.session_state: st.session_state.custom_tasks = []

# --- 3. DYNAMIC GREETINGS & QUOTES ---
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12: return "Good Morning, Jessica. Time to earn your keep."
    elif 12 <= hour < 18: return "Good Afternoon, Jessica. Don't let the momentum slide."
    else: return "Good Evening, Jessica. Finish strong. The Sanctuary is waiting."

negan_quotes = [
    "I appreciate you, Jessica. Now get back to work.",
    "People are counting on you. Take it like a champ.",
    "Documentation is the law of the land. Don't break it, Jess.",
    "Easy peasy lemon squeezy. Just get it done.",
    "You're the boss of this house. Act like it.",
    "I hope you have your shitting pants on, because we’ve got work to do."
]

# --- 4. MASTER FILENAMES (Verified from 1:48 AM List) ---
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

def trigger_voice(command_key):
    mapping = {
        "question": "all-you-gotta-do-is-answer-one-simple-question.mp3",
        "pick": "i-gotta-pick-somebody.mp3",
        "die": "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3",
        "logic": "i-know-it-s-not-easy-but-there-s-always-work-there-is-always-a-cost-here-if-you-try-to-skirt-it-if-you-try-to-cut-that-c.mp3",
        "win": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 5. HEADER SECTION ---
st.title("🏏 THE SANCTUARY")
st.write(f"### {get_greeting()}")
st.markdown(f'<div class="quote-box">"{random.choice(negan_quotes)}"</div>', unsafe_allow_html=True)

# Boss Mood UI
mood = st.session_state.boss_mood
if mood > 75: st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
else: st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 6. 🕹️ SURVIVAL GAMES (DOPAMINE HIT) ---
st.write("---")
g_col1, g_col2 = st.columns(2)
with g_col1:
    st.markdown('<div class="game-box">🎲 <b>SCAVENGE</b></div>', unsafe_allow_html=True)
    if st.button("BET 50 PTS"):
        if st.session_state.points >= 50:
            if random.random() > 0.5:
                st.session_state.points += 100
                st.success("💰 +100!")
                trigger_voice("win")
            else:
                st.session_state.points -= 50
                st.error("🧟 WALKER! -50")
                trigger_voice("die")
with g_col2:
    st.markdown('<div class="game-box">🏏 <b>ROULETTE</b></div>', unsafe_allow_html=True)
    if st.button("SPIN LUCILLE"):
        trigger_voice("pick")
        mod = random.choice([-20, 10, 50])
        st.session_state.points += mod
        st.info(f"SHIFT: {mod} pts")

# --- 7. 📜 FIELD ORDERS (MANUAL TASK ENTRY) ---
st.write("---")
st.write("### 📜 NEW FIELD ORDERS")
new_task = st.text_input("Assign a manual objective:", placeholder="Enter custom task...", label_visibility="collapsed")
if st.button("➕ ADD TO LOG"):
    if new_task:
        st.session_state.custom_tasks.append({"name": new_task, "done": False})
        trigger_voice("question")
        st.rerun()

# --- 8. MISSION LOG (FRI/SAT/SUN HOSPITAL MODE) ---
st.write("---")
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
st.write(f"### 🎯 MISSION LOG: {'HOSPITAL' if is_work else 'HOME BASE'}")

defaults = ["Handover & Meds", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee Recharge", "Groceries", "Base Maintenance", "Laundry"]

# Standard Tasks
for t in defaults:
    if st.button(f"✔️ {t}", key=f"def_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 5)
        st.toast(f"Secured: {t}")
        trigger_voice("random")

# Custom Manual Tasks
for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ CUSTOM: {ct['name']}", key=f"cust_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30
            trigger_voice("win")

# --- 9. THE VAULT (SIDEBAR REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Scavenge Points", f"{st.session_state.points} pts")
st.sidebar.write("---")
rewards = [
    ("☕ Premium Coffee", 20),
    ("🍺 Cold Cider", 40),
    ("🦶 Foot Massage", 80),
    ("🍽️ Fancy Dinner", 150),
    ("🛍️ Shopping Spree", 300)
]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.balloons()
            st.sidebar.success(f"CLAIMED: {name}")
        else: st.sidebar.error("Earn more points, Jessica.")

if st.sidebar.button("🔄 RESET ALL"):
    st.session_state.points = 0
    st.session_state.custom_tasks = []
    st.rerun()
