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

# --- NEGAN'S EXPANDED QUOTES ---
work_quotes = [
    "Jessica, people are counting on you. Take it like a champ.",
    "Chart now, relax later. Don't make me come down there.",
    "The hospital is a mess, but you? You're a goddamn rockstar.",
    "Documentation is the law of the land. Don't break the law.",
    "One med pass at a time, Jess. That's how we win.",
    "I appreciate you, Jessica. Now get back to work."
]
home_quotes = [
    "The girls are the future, Jessica. Protect the perimeter.",
    "Laundry is a choice. A choice I suggest you make.",
    "Easy peasy lemon squeezy. Just get the chores done.",
    "Coffee first, dominance second. That's the order of operations.",
    "The Sanctuary doesn't clean itself. Get moving.",
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

# --- RADIO TERMINAL: ALL 11 FILES ADDED ---
st.write("---")
st.write("### 📻 Savior Radio (Soundboard)")

# Mapped exactly from your Screenshot 2
negan_playlist = [
    "welcome-to-a-brand-new-beginning-you-sorry-shits.mp3",
    "do-not-make-me-have-to-ask.mp3",
    "i-think-you-re-going-to-be-up-to-speed-shortly.mp3",
    "i-m-gonna-need-you-to-do-it.mp3",
    "what-you-do-next-will-decide-whether-your-crap-d...yone-s-last-crap-day-or-just-another-crap-day.mp3",
    "we-re-getting-close.mp3",
    "oh-i-know-what-you-re-thinking.mp3",
    "i-m-negan.mp3",
    "here-goes-pay-attention.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-heard-in-my-life.mp3",
    "easy-peasy-lemon-squeezy.mp3"
]

col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 RANDOM ORDER"):
        chosen = random.choice(negan_playlist)
        if os.path.exists(chosen):
            st.audio(open(chosen, 'rb').read(), format='audio/mp3')
            st.caption(f"Playing: {chosen}")
        else:
            st.error("File not found. Check GitHub spelling!")

with col2:
    # This lets her pick a specific clip from a list
    selected_clip = st.selectbox("CHOOSE A CLIP:", negan_playlist)
    if st.button("▶️ PLAY SELECTED"):
        if os.path.exists(selected_clip):
            st.audio(open(selected_clip, 'rb').read(), format='audio/mp3')
        else:
            st.error("File not found on GitHub!")

# --- OBJECTIVES ---
st.write("---")
st.write("### 📝 Today's Objectives")
completed = 0
for task in tasks:
    if st.checkbox(f"**{task}**", key=f"task_{task}"):
        completed += 1

# --- REWARD VAULT ---
st.write("---")
points = completed * 20 
score = int((completed / len(tasks)) * 100) if tasks else 0

st.sidebar.title("💎 THE SCAVENGE VAULT")
st.sidebar.metric("Jess's Bank", f"{points} pts")
st.sidebar.write("---")
if points >= 20: st.sidebar.success("✅ **20pt: Premium Coffee/Tea**")
if points >= 40: st.sidebar.success("✅ **40pt: Cold Cider Drink**")
if points >= 60: st.sidebar.success("✅ **60pt: 30-Min Silence**")
if points >= 80: st.sidebar.success("✅ **80pt: 20-Min Foot Massage**")
if points >= 100: st.sidebar.success("🔥 **100pt: FANCY DINNER OUT**")

st.write(f"### Dominance Level: {score}%")
st.progress(score)

if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! Total dominance.'")

# --- CHOICE PARALYSIS ---
if st.button("🏏 LUCILLE, CHOOSE MY FATE"):
    st.warning(f"Lucille says: **{random.choice(tasks)}**. NOW.")
