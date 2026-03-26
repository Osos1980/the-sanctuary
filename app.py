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

# --- NEGAN'S EXPANDED QUOTE VARIETY ---
work_quotes = [
    "Jessica, people are counting on you. Take it like a champ.",
    "Chart now, relax later. Don't make me come down there.",
    "The hospital is a mess, but you? You're a goddamn rockstar.",
    "I appreciate you, Jessica. Now get back to work.",
    "You save lives. Now save your sanity and finish these tasks!",
    "One med pass at a time, Jess. That's how we win.",
    "Documentation is the law of the land. Don't break the law."
]

home_quotes = [
    "The girls are the future, Jessica. Protect the perimeter.",
    "Laundry is a choice. A choice I suggest you make.",
    "I'm bored, Jess. Go do a 'scavenge run' (Groceries).",
    "Easy peasy lemon squeezy. Just get the chores done.",
    "The Sanctuary doesn't clean itself. Get moving.",
    "Coffee first, dominance second. That's the order of operations.",
    "You're the boss of this house. Act like it."
]

# --- APP HEADER ---
st.title("🏏 THE SANCTUARY")
st.write(f"### **Current Status:** {today}")

if is_work_day:
    st.error("🚨 **MISSION: THE FRONT LINES (Hospital Mode)**")
    quote = random.choice(work_quotes)
    tasks = ["Handover & Initial Med Pass", "Mid-Shift Charting (Stay sharp!)", "Hydration/Sanity Break", "Safety Checks & Final Rounds", "Decompression Drive Home"]
else:
    st.success("🏠 **MISSION: HOME BASE (Logistics Mode)**")
    quote = random.choice(home_quotes)
    tasks = ["School/Activity Drop-off", "Coffee Recharge", "The Scavenge (Groceries)", "Base Maintenance (Cleaning)", "The Kid Pickup"]

st.info(f"🗨️ **THE BOSS SAYS:** \"{quote}\"")

# --- RADIO TERMINAL: ALL 7 VOICES ADDED ---
st.write("---")
st.write("### 📻 Savior Radio (Listen for Orders)")

# These match your screenshot filenames exactly
negan_clips = [
    "do-not-let-me-distract-you-young-man.mp3",
    "easy-peasy-lemon-squeezy.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-seen.mp3",
    "here-goes-pay-attention.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-m-negan.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-mind.mp3"
]

if st.button("🔊 TRANSMIT RANDOM ORDERS"):
    # This picks a random one from the 7 every time she clicks
    chosen = random.choice(negan_clips)
    if os.path.exists(chosen):
        st.audio(open(chosen, 'rb').read(), format='audio/mp3')
        st.caption(f"📢 Now Playing: {chosen.replace('-', ' ').replace('.mp3', '')}")
    else:
        # If the filename was shortened by GitHub, this tries the shortened version
        short_name = chosen.replace("ever-seen", "...").replace("mind", "...")
        if os.path.exists(short_name):
             st.audio(open(short_name, 'rb').read(), format='audio/mp3')
        else:
            st.warning("⚠️ Signal lost. Ensure filenames on GitHub match the script!")

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

if points >= 20: st.sidebar.success("✅ **20pt: Premium Coffee/Tea** ☕")
if points >= 40: st.sidebar.success("✅ **40pt: Cold Cider Drink** 🍺")
if points >= 60: st.sidebar.success("✅ **60pt: 30-Min Uninterrupted Silence** 🤫")
if points >= 80: st.sidebar.success("✅ **80pt: 20-Min Foot Massage** 🦶")
if points >= 100: st.sidebar.success("🔥 **100pt: FANCY DINNER OUT** 🍷")

st.write(f"### Dominance Level: {score}%")
st.progress(score)

if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! Total dominance. I knew you could do it.'")

# --- CHOICE PARALYSIS TOOL ---
st.write("---")
if st.button("🏏 LUCILLE, CHOOSE MY FATE"):
    st.warning(f"Lucille has spoken: **{random.choice(tasks)}**. No excuses!")
