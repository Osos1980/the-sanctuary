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
    .game-box { padding: 15px; border: 1px solid #ff4b4b; border-radius: 15px; background-color: #1e2129; margin-bottom: 10px; text-align: center; }
    .stTextInput>div>div>input { background-color: #1e2129; color: white; border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT STATE ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50
if "custom_tasks" not in st.session_state: st.session_state.custom_tasks = []

# --- 3. MASTER FILENAMES (Verified from 1:48 AM Screenshot) ---
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
        "win": "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
        "snark": "are-you-kidding-me.mp3",
        "cooperate": "are-you-cooperating.mp3"
    }
    file = mapping.get(command_key, random.choice(negan_playlist))
    if os.path.exists(file):
        st.audio(open(file, 'rb').read(), format='audio/mp3')

# --- 4. HEADER & DYNAMIC QUOTES ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica")

mood = st.session_state.boss_mood
if mood > 75: 
    st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
    st.info("Boss Quote: 'I appreciate you, Jessica. Now get back to work.'")
elif mood > 40: 
    st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
    st.info("Boss Quote: 'People are counting on you. Take it like a champ.'")
else: 
    st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")
    st.info("Boss Quote: 'I hope you have your shitting pants on.'")

# --- 5. 🕹️ SURVIVAL GAMES (Double or Nothing) ---
st.write("---")
g_col1, g_col2 = st.columns(2)
with g_col1:
    st.markdown('<div class="game-box"><b>🎲 SCAVENGE</b></div>', unsafe_allow_html=True)
    if st.button("Risk 50 Pts"):
        if st.session_state.points >= 50:
            if random.random() > 0.5:
                st.session_state.points += 100
                st.success("JACKPOT! +100")
                trigger_voice("win")
            else:
                st.session_state.points -= 50
                st.error("WALKERS! -50")
                trigger_voice("die")
with g_col2:
    st.markdown('<div class="game-box"><b>🏏 ROULETTE</b></div>', unsafe_allow_html=True)
    if st.button("Spin Lucille"):
        trigger_voice("pick")
        mod = random.choice([-20, 10, 50])
        st.session_state.points += mod
        st.info(f"Point Shift: {mod}")

# --- 6. 📝 FIELD ORDERS (ADD MANUAL TASKS) ---
st.write("---")
st.write("### 📜 NEW FIELD ORDERS")
new_task = st.text_input("Enter a custom objective:", placeholder="e.g., Call insurance, extra med pass...")
if st.button("➕ ADD TO MISSION LOG"):
    if new_task:
        st.session_state.custom_tasks.append({"name": new_task, "done": False})
        trigger_voice("question")
        st.rerun()

# --- 7. MISSION LOG (HOSPITAL VS HOME) ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")
today = datetime.datetime.now().strftime("%A")
is_work = today in ["Friday", "Saturday", "Sunday"]
defaults = ["Med Pass", "Charting", "Hydration", "Safety Checks", "Drive Home"] if is_work else ["Coffee", "Groceries", "Cleaning", "Pickup"]

for t in defaults:
    if st.button(f"✔️ {t}", key=f"def_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 5)
        st.toast(f"Secured: {t}")
        trigger_voice("random")

# Show Jessica's Manual Tasks
for i, ct in enumerate(st.session_state.custom_tasks):
    if not ct["done"]:
        if st.button(f"⭐ CUSTOM: {ct['name']}", key=f"cust_{i}"):
            st.session_state.custom_tasks[i]["done"] = True
            st.session_state.points += 30
            trigger_voice("win")

# --- 8. THE VAULT (REWARDS) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points", f"{st.session_state.points}")
st.sidebar.write("---")
rewards = [("☕ Coffee", 20), ("🍺 Cider", 40), ("🦶 Massage", 80), ("🍽️ Dinner", 150), ("🛍️ Shopping", 300)]
for name, cost in rewards:
    if st.sidebar.button(f"{name} ({cost})"):
        if st.session_state.points >= cost:
            st.session_state.points -= cost
            st.sidebar.balloons()
        else: st.sidebar.error("Earn more points.")

if st.sidebar.button("🔄 RESET ALL"):
    st.session_state.points = 0
    st.session_state.custom_tasks = []
    st.rerun()
