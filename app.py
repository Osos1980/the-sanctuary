import streamlit as st
import datetime
import pytz
import random
import time
import json
import os

# --- CONFIG ---
st.set_page_config(page_title="Jessica's Sanctuary", page_icon="🏏", layout="centered")
SAVE_FILE = "sanctuary_save.json"

# --- STYLE ---
st.markdown("""
<style>
.main { background:#0e1117; color:white; }
.stButton>button {
    width:100%; height:60px; font-size:18px;
    border-radius:15px; background:#ff4b4b;
    color:white; font-weight:bold;
}
.negan-box {
    background:#1e2129; padding:15px;
    border-left:6px solid #ff4b4b;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
def load_data():
    if os.path.exists(SAVE_FILE):
        try: return json.load(open(SAVE_FILE))
        except: return {}
    return {}

def save_data():
    safe = {k:v for k,v in st.session_state.items()
            if isinstance(v,(int,float,str,list,dict,bool))}
    json.dump(safe, open(SAVE_FILE,"w"))

data = load_data()

def init(k,v):
    if k not in st.session_state:
        st.session_state[k] = data.get(k,v)

# --- STATE ---
init("points",100)
init("xp",0)
init("level",1)
init("completed_tasks",[])
init("manual_tasks",[])
init("boss_hp",100)
init("last_day","")
init("last_msg","Waiting on you, Jessica.")
init("combo",0)
init("last_task_time",time.time())
init("last_interrupt",0)
init("weekly",[0]*7)
init("last_jess_quote","")
init("last_quote_time",0)
init("custom_rewards",[])
init("last_reward_claim",0)

# --- TIME ---
central = pytz.timezone('US/Central')
now = datetime.datetime.now(central)
today = str(now.date())
weekday = now.weekday()
hour = now.hour

# --- DAILY RESET ---
if st.session_state.last_day != today:
    st.session_state.completed_tasks = []
    st.session_state.last_day = today
    st.session_state.last_msg = random.choice([
        "Rise and shine.",
        "Let's get to work.",
        "New day. My rules."
    ])
    save_data()

# --- VOICE ---
def negan_speak(text):
    st.session_state.last_msg = text
    st.toast(text)
    st.markdown(f"""
    <script>
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.rate=0.85; msg.pitch=0.6;
    speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# --- JESS QUOTES ---
JESS_QUOTES = [
    "Jessica, just start small.",
    "One task changes everything.",
    "Momentum beats perfection.",
    "You're capable. Move.",
    "Future you will thank you.",
]

# --- HEADER ---
st.title("🏏 THE SANCTUARY")

col1,col2 = st.columns([1,3])

with col1:
    if os.path.exists("negan.png"):
        st.image("negan.png", use_container_width=True)

with col2:
    st.markdown(f"""<div class="negan-box">🧟 "{st.session_state.last_msg}"</div>""", unsafe_allow_html=True)

# --- MOTIVATION ---
if time.time() - st.session_state.last_quote_time > 120:
    q = random.choice(JESS_QUOTES)
    if q != st.session_state.last_jess_quote:
        st.session_state.last_jess_quote = q
        st.session_state.last_quote_time = time.time()
        st.info(f"💬 {q}")

# --- INTERRUPT ---
if time.time() - st.session_state.last_interrupt > random.randint(180,300):
    st.session_state.last_interrupt = time.time()
    msg = random.choice(["Do one task now.","Move.","Stop stalling.","2 min clean."])
    st.error(f"⚠️ {msg}")
    negan_speak(msg)

# --- STATS ---
c1,c2,c3 = st.columns(3)
c1.metric("LEVEL",st.session_state.level)
c2.metric("POINTS",st.session_state.points)
c3.metric("BOSS",f"{st.session_state.boss_hp}%")
st.progress(st.session_state.xp/100)

# --- MISSIONS ---
st.write("## 🎯 MISSIONS")

with st.expander("➕ ADD MISSION"):
    new_task = st.text_input("Mission")
    if st.button("ADD"):
        if new_task:
            st.session_state.manual_tasks.append(new_task)
            negan_speak(f"Mission added: {new_task}")
            save_data()
            st.rerun()

tasks = ["Coffee","Clean","Laundry","Reset"] + st.session_state.manual_tasks

for t in tasks:
    if t not in st.session_state.completed_tasks:
        if st.button(f"✔️ {t}", key=t):
            now_t = time.time()
            if now_t - st.session_state.last_task_time < 120:
                st.session_state.combo += 1
            else:
                st.session_state.combo = 1

            bonus = st.session_state.combo * 5

            st.session_state.completed_tasks.append(t)
            st.session_state.points += 25 + bonus
            st.session_state.xp += 20 + bonus
            st.session_state.weekly[weekday] += 1

            if random.random()>0.5:
                st.info(f"💬 {random.choice(JESS_QUOTES)}")

            negan_speak("Good." if st.session_state.combo<3 else "Momentum.")

            if st.session_state.xp>=100:
                st.session_state.level+=1
                st.session_state.xp=0
                negan_speak("Level up.")

            st.session_state.last_task_time = now_t
            save_data()
            st.rerun()
    else:
        st.button(f"✅ {t}",disabled=True,key=f"d{t}")

    if t in st.session_state.manual_tasks:
        if st.button(f"❌ Remove {t}",key=f"rm{t}"):
            st.session_state.manual_tasks.remove(t)
            save_data()
            st.rerun()

# --- FOCUS ---
st.write("## ⏱️ FOCUS")
if st.button("2 MIN"):
    st.session_state.timer = time.time()
    st.session_state.timer_len = 120
if st.button("5 MIN"):
    st.session_state.timer = time.time()
    st.session_state.timer_len = 300

if "timer" in st.session_state:
    remain = max(0, st.session_state.timer_len - int(time.time()-st.session_state.timer))
    st.write(remain)
    if remain==0:
        st.session_state.xp += 30
        negan_speak("Focus complete.")
        del st.session_state.timer

# --- GAMES ---
st.write("## 🎮")
if st.button("⚔️ ATTACK"):
    dmg=random.randint(20,40)
    st.session_state.boss_hp -= dmg
    if st.session_state.boss_hp<=0:
        st.session_state.boss_hp=100
        st.session_state.points+=100
        st.balloons()
        negan_speak("Boss down.")

if st.button("🔦 SCAVENGE"):
    if st.session_state.points>=20:
        st.session_state.points-=20
        if random.random()>0.5:
            win=random.randint(40,80)
            st.session_state.points+=win
            negan_speak("Jackpot.")
        else:
            negan_speak("Nothing.")

# --- SMART REWARD VAULT ---
with st.sidebar:
    st.title("💎 REWARD VAULT")
    st.metric("Points", st.session_state.points)

    base_rewards = [
        {"name":"☕ Coffee","cost":50},
        {"name":"📺 Show","cost":100},
        {"name":"🛁 Reset","cost":150},
        {"name":"🎮 Chill","cost":300},
    ]

    # --- CONTEXT-AWARE ---
    st.write("### 🧠 SUGGESTED")

    if hour >= 21:
        suggestion = {"name":"😴 Sleep / Rest","cost":40}
    elif st.session_state.combo >= 4:
        suggestion = {"name":"🔥 Big Reward","cost":200}
    elif st.session_state.combo >= 2:
        suggestion = {"name":"⚡ Quick Break","cost":80}
    else:
        suggestion = {"name":"🧠 Small Reset","cost":40}

    st.info(f"{suggestion['name']} ({suggestion['cost']})")

    if st.session_state.points >= suggestion["cost"]:
        if st.button("CLAIM SUGGESTED"):
            st.session_state.points -= suggestion["cost"]
            negan_speak("Smart choice.")
            save_data()
            st.rerun()

    # --- CUSTOM REWARDS ---
    with st.expander("➕ CUSTOM REWARD"):
        name = st.text_input("Reward name")
        cost = st.number_input("Cost", min_value=10)
        if st.button("ADD REWARD"):
            st.session_state.custom_rewards.append({"name":name,"cost":cost})
            save_data()
            st.rerun()

    st.write("### 🎁 ALL REWARDS")
    rewards = base_rewards + st.session_state.custom_rewards

    for i,r in enumerate(rewards):
        if st.session_state.points >= r["cost"]:
            if st.button(f"✅ {r['name']} ({r['cost']})",key=f"r{i}"):
                st.session_state.points -= r["cost"]

                if random.random()>0.7:
                    bonus=random.randint(10,50)
                    st.session_state.points += bonus
                    st.success(f"Bonus +{bonus}")

                negan_speak("Earned.")
                save_data()
                st.rerun()
        else:
            st.markdown(f"🔒 {r['name']} — {r['cost']}")

        if r in st.session_state.custom_rewards:
            if st.button(f"❌ Remove {r['name']}",key=f"rr{i}"):
                st.session_state.custom_rewards.remove(r)
                save_data()
                st.rerun()

    if st.button("RESET"):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()

# --- SNAP ---
if st.button("🧠 SNAP ME OUT OF IT"):
    msg=random.choice(["Do one task","Move","Drink water"])
    st.error(msg)
    negan_speak(msg)

# --- WEEKLY ---
st.write("## 📊 WEEKLY")
cols = st.columns(7)
for i,v in enumerate(st.session_state.weekly):
    cols[i].metric(str(i+1),v)
