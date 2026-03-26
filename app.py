import streamlit as st
import datetime
import random

# --- THEME SETTINGS ---
st.set_page_config(page_title="The Sanctuary", page_icon="🏒")
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .stButton>button { background-color: #444; color: red; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC: WHAT DAY IS IT? ---
today = datetime.datetime.now().strftime("%A")
work_days = ["Friday", "Saturday", "Sunday"]
is_work_day = today in work_days

# --- NEGAN'S DATABASE ---
work_quotes = ["Jessica, people are counting on you. Take it like a champ.", "Chart now, relax later. Don't make me come down there.", "You're the boss of this ward, Jess."]
home_quotes = ["The girls are the future, Jessica. Protect the perimeter.", "I'm bored, Jess. Go do a 'scavenge run' (Groceries).", "Laundry is a choice. A choice I suggest you make."]

# --- APP LAYOUT ---
st.title("🏒 THE SANCTUARY")
st.subheader(f"Welcome back, Jessica. It's {today}.")

if is_work_day:
    st.error("🚨 MISSION: THE FRONT LINES (Hospital)")
    quote = random.choice(work_quotes)
    tasks = ["Handover / Med Pass", "Patient Charting (Don't fall behind!)", "12:00 PM Hydration Break", "Final Rounds", "The 'I Survived' Decompression"]
else:
    st.success("🏡 MISSION: HOME BASE (Logistics)")
    quote = random.choice(home_quotes)
    tasks = ["School Drop-off", "Coffee Recharge", "The Scavenge (Groceries/Errands)", "Sanctuary Maintenance (Cleaning)", "The Pickup"]

st.info(f"**Negan:** '{quote}'")

# --- TASK LIST ---
st.write("### 📝 Today's Orders")
completed = 0
for task in tasks:
    if st.checkbox(task):
        completed += 1

# --- THE "EENY MEENY" CHOICE PARALYSIS TOOL ---
st.write("---")
if st.button("LUCILLE, PICK FOR ME"):
    pick = random.choice(tasks)
    st.warning(f"Lucille says: **{pick}**. No excuses, Jessica.")

# --- REWARD TRACKER ---
score = int((completed / len(tasks)) * 100)
st.write(f"### Current Dominance: {score}%")
st.progress(score)

if score == 100:
    st.balloons()
    st.success("🔥 'Hot diggity dog! You did it, Jess! Go put your feet up.'")