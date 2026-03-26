import streamlit as st
import datetime
import random
import os

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 50px; height: 3.5em; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #ff3333; border: 1px solid white; box-shadow: 0px 0px 15px #ff4b4b; }
    h1, h2, h3 { color: #ff4b4b; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT DATA ---
if "points" not in st.session_state: st.session_state.points = 0
if "boss_mood" not in st.session_state: st.session_state.boss_mood = 50

# --- 3. JESSICA'S PERSONALIZED QUOTES & LOGIC ---
today = datetime.datetime.now().strftime("%A")
is_work_day = today in ["Friday", "Saturday", "Sunday"]

# Quotes for the top of the app
work_quotes = [
    "Jessica, people are counting on you. Take it like a champ.",
    "The hospital is a mess, but you? You're a goddamn rockstar.",
    "Documentation is the law of the land. Don't break it, Jess.",
    "I appreciate you, Jessica. Now get back to work."
]
home_quotes = [
    "The girls are the future, Jessica. Protect the perimeter.",
    "Easy peasy lemon squeezy. Just get the chores done.",
    "You're the boss of this house. Act like it.",
    "The Sanctuary doesn't clean itself. Get moving, Jess."
]

# --- 4. THE 9 FILENAMES (From Screenshot 1:48 AM) ---
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

def play_radio():
    clip = random.choice(negan_playlist)
    if os.path.exists(clip):
        st.audio(open(clip, 'rb').read(), format='audio/mp3')
    else:
        st.sidebar.error(f"Signal Lost: {clip}")

# --- 5. HEADER & MOOD ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Commander:** Jessica | **Status:** {today}")

# Display the personalized quote
current_quote = random.choice(work_quotes if is_work_day else home_quotes)
st.info(f"🗨️ **THE BOSS SAYS:** \"{current_quote}\"")

# Mood System
mood = st.session_state.boss_mood
if mood > 75: st.success(f"😎 NEGAN'S MOOD: Damn proud of you, Jess ({mood}%)")
elif mood > 40: st.warning(f"😐 NEGAN'S MOOD: Watching your back, Jess ({mood}%)")
else: st.error(f"💀 NEGAN'S MOOD: Don't make him ask twice, Jess ({mood}%)")

# --- 6. MISSIONS ---
st.write("---")
st.write("### 🎯 ACTIVE OBJECTIVES")

if is_work_day:
    tasks = ["Handover & Med Pass", "Charting (Don't let 'em catch you, Jess!)", "Hydration Break", "Safety Checks", "Drive Home Decompression"]
else:
    tasks = ["Girls Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance", "The Girls Pickup"]

for t in tasks:
    if st.button(f"✔️ {t}", key=f"btn_{t}"):
        st.session_state.points += 20
        st.session_state.boss_mood = min(100, st.session_state.boss_mood + 10)
        st.toast(f"Good work, Jessica. {t} complete.")
        play_radio()

# --- 7. CHAOS TOOLS ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏏 LUCILLE DECIDES"):
        st.warning(f"JESSICA, DO THIS NOW: {random.choice(tasks)}")
        play_radio()
with c2:
    if st.button("⚡ JESS'S SPEED RUN"):
        st.error("⏱️ 10 MINUTES. GO! NO THINKING.")

# --- 8. REWARDS VAULT (SIDEBAR) ---
st.sidebar.title("💎 JESSICA'S VAULT")
st.sidebar.metric("Points Bank", f"{st.session_state.points} pts")
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
        else:
            st.sidebar.error("Earn more points, Jessica.")

if st.sidebar.button("🔄 RESET DAY"):
    st.session_state.boss_mood = 50
    st.rerun()
