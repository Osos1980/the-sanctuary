import streamlit as st
import datetime
import random

# --- THEME & CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏")

# Custom CSS for a "Saviors" Dark Mode look
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .stCheckbox { font-size: 20px; padding: 10px; background: #262626; border-radius: 5px; margin-bottom: 5px; }
    .stButton>button { width: 100%; background-color: #444; color: #ff4b4b; border: 2px solid #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: WORK VS HOME ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- NEGAN'S ORDERS DATABASE ---
work_quotes = [
    "Jessica, people are counting on you. Take it like a champ.",
    "Chart now, relax later. Don't make me come down there.",
    "You're the boss of this ward, Jess. Act like it.",
    "I appreciate you, Jessica. Now get back to work."
]
home_quotes = [
    "The girls are the future, Jessica. Protect the perimeter.",
    "I'm bored, Jess. Go do a 'scavenge run' (Groceries).",
    "Laundry is a choice. A choice I suggest you make.",
    "Easy peasy lemon squeezy. Just get the chores done."
]

# --- APP HEADER ---
st.title("🏏 THE SANCTUARY")
st.subheader(f"Status Report: {today}")

if is_work_day:
    st.error("🚨 MISSION: THE FRONT LINES (Hospital)")
    quote = random.choice(work_quotes)
    tasks = ["Handover & Med Pass", "Patient Charting (Stay ahead!)", "Hydration Break (Orders!)", "Final Rounds", "Decompression Drive Home"]
else:
    st.success("🏠 MISSION: HOME BASE (Logistics)")
    quote = random.choice(home_quotes)
    tasks = ["School/Activity Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Sanctuary Maintenance (Cleaning)", "The Kid Pickup"]

st.info(f"**Negan says:** '{quote}'")

# --- RADIO TERMINAL (Voice Section) ---
st.write("---")
st.write("### 📻 Sanctuary Radio")
# To make this work, upload a file named 'negan.mp3' to your GitHub
if st.button("🔊 PLAY LATEST ORDERS"):
    try:
        audio_file = open('negan.mp3', 'rb')
        st.audio(audio_file.read(), format='audio/mp3')
    except FileNotFoundError:
        st.warning("Radio Silence. (Upload 'negan.mp3' to GitHub to hear the boss!)")

# --- TASK LIST ---
st.write("---")
st.write("### 📝 Today's Objectives")
completed = 0
for task in tasks:
    if st.checkbox(task, key=task):
        completed += 1

# --- PROGRESS & REWARDS ---
st.write("---")
score = int((completed / len(tasks)) * 100) if tasks else 0
st.write(f"### Dominance Level: {score}%")
st.progress(score)

# Sidebar Rewards (The Incentive)
points = completed * 10
st.sidebar.title("💎 Scavenge Points")
st.sidebar.metric("Jessica's Points", f"{points} pts")

st.sidebar.write("---")
st.sidebar.write("### Available Rewards")
if points >= 30:
    st.sidebar.success("🔓 30pt: Foot Massage")
if points >= 50:
    st.sidebar.success("🔓 50pt: Choice of Dinner")
if points >= 100:
    st.sidebar.success("🔓 100pt: Total Day Off")

# Final Win Condition
if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! You did it, Jess! Go put your feet up.'")

# --- THE CHOICE PARALYSIS TOOL ---
if st.button("LUCILLE, PICK FOR ME"):
    pick = random.choice(tasks)
    st.warning(f"Lucille has spoken: **{pick}**. No excuses.")
