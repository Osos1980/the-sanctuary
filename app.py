import streamlit as st
import datetime
import random
import os

# --- THEME & CONFIG ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏏")

# Custom CSS for the "Saviors" aesthetic
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .stCheckbox { font-size: 18px; padding: 8px; background: #262626; border-radius: 8px; margin-bottom: 5px; }
    .stButton>button { width: 100%; background-color: #444; color: #ff4b4b; border: 2px solid #ff4b4b; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: WORK VS HOME ---
# Since it is now Thursday night/Friday morning, the app will switch modes automatically.
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- NEGAN'S TEXT DATABASE ---
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

# --- RADIO TERMINAL (The Sounds You Uploaded) ---
st.write("---")
st.write("### 📻 Sanctuary Radio")

# Updated list with full names and shortened names just in case
negan_clips = [
    "do-not-let-me-distract-you-young-man.mp3",
    "easy-peasy-lemon-squeezy.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-ever-seen.mp3",
    "god-damn-it-that-is-the-coolest-thing-i-ve-...mp3", 
    "here-goes-pay-attention.mp3",
    "i-gotta-pick-somebody.mp3",
    "i-m-negan.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-mind.mp3",
    "i-want-you-to-hear-that-again-if-you-don-t-...mp3"
]

if st.button("🔊 HEAR THE BOSS"):
    # Filter only the files that actually exist on your GitHub right now
    available_clips = [f for f in negan_clips if os.path.exists(f)]
    
    if available_clips:
        chosen_clip = random.choice(available_clips)
        audio_file = open(chosen_clip, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')
        st.caption(f"Playing: {chosen_clip}")
    else:
        st.error("Radio Silence. GitHub filenames don't match. Click a file on GitHub to see its full name!")

# --- TASK LIST ---
st.write("---")
st.write("### 📝 Today's Objectives")
completed = 0
for task in tasks:
    if st.checkbox(task, key=f"check_{task}"):
        completed += 1

# --- PROGRESS & REWARDS ---
st.write("---")
score = int((completed / len(tasks)) * 100) if tasks else 0
st.write(f"### Dominance Level: {score}%")
st.progress(score)

# Sidebar Rewards
points = completed * 10
st.sidebar.title("💎 Scavenge Points")
st.sidebar.metric("Jessica's Points", f"{points} pts")
st.sidebar.write("---")
st.sidebar.write("### Available Rewards")
if points >= 30: st.sidebar.success("🔓 30pt: Foot Massage")
if points >= 50: st.sidebar.success("🔓 50pt: Choice of Dinner")
if points >= 100: st.sidebar.success("🔓 100pt: Total Day Off")

if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! You did it, Jess! Go put your feet up.'")

# --- THE CHOICE PARALYSIS TOOL ---
st.write("---")
if st.button("🏏 LUCILLE, PICK FOR ME"):
    pick = random.choice(tasks)
    st.warning(f"Lucille has spoken: **{pick}**. No excuses.")
