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
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border: none; font-weight: bold; font-size: 1.2em; border-radius: 50px; height: 3.5em; box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: DATE CHECK ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- NEGAN'S COMMENTARY ---
if is_work_day:
    st.error(f"🚨 **MISSION: THE FRONT LINES ({today})**")
    tasks = ["Handover & Initial Med Pass", "Mid-Shift Charting (Stay sharp!)", "Hydration/Sanity Break", "Safety Checks & Final Rounds", "Decompression Drive Home"]
    quotes = ["People are counting on you, Jess. Take it like a champ.", "Finish the shift, earn the spoils.", "You're a rockstar. Now act like it."]
else:
    st.success(f"🏠 **MISSION: HOME BASE ({today})**")
    tasks = ["School/Activity Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance (Cleaning)", "The Kid Pickup"]
    quotes = ["The girls are the future. Protect the perimeter.", "Laundry is a choice. I suggest you make it.", "Easy peasy lemon squeezy."]

st.info(f"🗨️ **THE BOSS SAYS:** \"{random.choice(quotes)}\"")

# --- RADIO TERMINAL ---
st.write("---")
st.write("### 📻 Savior Radio")
negan_clips = [
    "do-not-let-me-distract-you-young-man.mp3", "easy-peasy-lemon-squeezy.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-seen.mp3", "god-damn-it-that-is-the-coolest-thing-i-ve-...mp3", 
    "here-goes-pay-attention.mp3", "i-gotta-pick-somebody.mp3", "i-m-negan.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-mind.mp3", "i-want-you-to-hear-that-again-if-you-don-t-...mp3"
]

if st.button("🔊 TRANSMIT ORDERS"):
    available = [f for f in negan_clips if os.path.exists(f)]
    if available:
        chosen = random.choice(available)
        st.audio(open(chosen, 'rb').read(), format='audio/mp3')
    else:
        st.warning("⚠️ Radio Static. Check GitHub filenames!")

# --- OBJECTIVES ---
st.write("---")
st.write("### 📝 Today's Objectives")
completed = 0
for task in tasks:
    if st.checkbox(f"**{task}**", key=f"task_{task}"):
        completed += 1

# --- THE EXPANDED REWARD VAULT ---
st.write("---")
points = completed * 20 
score = int((completed / len(tasks)) * 100) if tasks else 0

st.sidebar.title("💎 THE SCAVENGE VAULT")
st.sidebar.metric("Jess's Bank", f"{points} pts")
st.sidebar.write("---")
st.sidebar.subheader("🔓 EARNED TODAY")

# The Reward Tiers
if points >= 20:
    st.sidebar.success("✅ **20pt: Premium Coffee/Tea** ☕")
if points >= 40:
    st.sidebar.success("✅ **40pt: Cold Cider Drink** 🍺")
if points >= 60:
    st.sidebar.success("✅ **60pt: 30-Min Uninterrupted Silence** 🤫")
if points >= 80:
    st.sidebar.success("✅ **80pt: 20-Min Foot Massage** 🦶")
if points >= 100:
    st.sidebar.success("🔥 **100pt: FANCY DINNER OUT** 🍷")
    st.sidebar.caption("Pick the place. I'm paying.")

# Progress Bar
st.write(f"### Dominance Level: {score}%")
st.progress(score)

if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! Total dominance. Get dressed, we're going to dinner.'")

# --- CHOICE PARALYSIS TOOL ---
st.write("---")
if st.button("🏏 LUCILLE, CHOOSE MY FATE"):
    st.warning(f"Lucille has spoken: **{random.choice(tasks)}**. Move it!")
