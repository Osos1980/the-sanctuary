import streamlit as st
import datetime
import random
import os

# --- THEME & UI ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stCheckbox { font-size: 20px; padding: 12px; background: #1c1c1c; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 8px; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border: none; font-weight: bold; font-size: 1.1em; border-radius: 50px; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: DATE CHECK ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- NEGAN'S TEXT VARIETY ---
work_quotes = [
    "Jessica, people are counting on you. Take it like a champ.",
    "Chart now, relax later. Don't make me come down there.",
    "The hospital is a mess, but you? You're a goddamn rockstar.",
    "Documentation is the law of the land. Don't break it.",
    "I appreciate you, Jessica. Now get back to work."
]
home_quotes = [
    "The girls are the future, Jessica. Protect the perimeter.",
    "Laundry is a choice. A choice I suggest you make.",
    "Easy peasy lemon squeezy. Just get the chores done.",
    "The Sanctuary doesn't clean itself. Get moving.",
    "You're the boss of this house. Act like it."
]

# --- APP HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Current Status:** {today}")

if is_work_day:
    st.error("🚨 **MISSION: THE FRONT LINES (Hospital Mode)**")
    tasks = ["Handover & Initial Med Pass", "Mid-Shift Charting (Stay sharp!)", "Hydration/Sanity Break", "Safety Checks & Final Rounds", "Decompression Drive Home"]
else:
    st.success("🏠 **MISSION: HOME BASE (Logistics Mode)**")
    tasks = ["School/Activity Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance (Cleaning)", "The Kid Pickup"]

st.info(f"🗨️ **THE BOSS SAYS:** \"{random.choice(work_quotes if is_work_day else home_quotes)}\"")

# --- RADIO TERMINAL: MATCHING SCREENSHOT 1.24.14 AM ---
st.write("---")
st.write("### 📻 Savior Radio (Soundboard)")

# Exact mapping from your latest file list
negan_playlist = [
    "all-you-gotta-do-is-answer-one-simple-question.mp3",
    "do-not-let-me-distract-you-young-man.mp3",
    "easy-peasy-lemon-squeezy.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
    "here-goes-pay-attention.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-m-negan.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-have-something-interesting-for-us-somebody-s-going-to-die.mp3"
]

selected_clip = st.selectbox("CHOOSE A COMMAND:", negan_playlist)

if st.button("▶️ BROADCAST ORDERS"):
    if os.path.exists(selected_clip):
        with open(selected_clip, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        st.success(f"Playing: {selected_clip}")
    else:
        st.error(f"❌ File '{selected_clip}' not found. Check if it's in the same folder as app.py!")

# --- OBJECTIVES & REWARDS ---
st.write("---")
st.write("### 📝 Today's Objectives")
completed = 0
for task in tasks:
    if st.checkbox(f"**{task}**", key=f"task_{task}"):
        completed += 1

points = completed * 20 
st.sidebar.title("💎 SCAVENGE VAULT")
st.sidebar.metric("Jess's Bank", f"{points} pts")
st.sidebar.write("---")
if points >= 20: st.sidebar.success("✅ **20pt: Premium Coffee/Tea**")
if points >= 40: st.sidebar.success("✅ **40pt: Cold Cider Drink**")
if points >= 60: st.sidebar.success("✅ **60pt: 30-Min Silence**")
if points >= 80: st.sidebar.success("✅ **80pt: 20-Min Foot Massage**")
if points >= 100: st.sidebar.success("🔥 **100pt: FANCY DINNER OUT**")

st.progress(int((completed / len(tasks)) * 100) if tasks else 0)

# --- CHOICE PARALYSIS TOOL ---
if st.button("🏏 LUCILLE, CHOOSE MY FATE"):
    st.warning(f"Lucille says: **{random.choice(tasks)}**. No excuses!")

# --- QUICK DEBUGGER ---
with st.expander("🛠️ Folder Check"):
    st.write("Files currently in Sanctuary folder:", os.listdir("."))
