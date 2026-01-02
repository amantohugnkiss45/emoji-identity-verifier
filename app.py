import streamlit as st
import hashlib
import time

# --- 1. GLOBAL SERVER MEMORY ---
# This function creates a shared object in the server's RAM.
# All users visiting your URL will share this same counter.
@st.cache_resource
def get_global_ticker():
    return {"count": 0}

ticker = get_global_ticker()

# --- 2. CONFIGURATION ---
EMOJI_POOL = ["😀(grinning-face)",
"😃(grinning-face-with-big-eyes)",
"😄(grinning-face-with-smiling-eyes)",
"😁(beaming-face-with-smiling-eyes)",
"😆(grinning-squinting-face)",
"😅(grinning-face-with-sweat)",
"😂(face-with-tears-of-joy)",
"🤣(rolling-on-the-floor-laughing)",
"😊(smiling-face-with-smiling-eyes)",
"😇(smiling-face-with-halo)",
"🥰(smiling-face-with-hearts)",
"😍(smiling-face-with-heart-eyes)",
"🤩(star-struck)",
"😘(face-blowing-a-kiss)",
"😗(kissing-face)",
"☺️(smiling-face)",
"😋(face-savoring-food)",
"😛(face-with-tongue)",
"😜(winking-face-with-tongue)",
"🤪(zany-face)",
"🤨(face-with-raised-eyebrow)",
"🧐(face-with-monocle)",
"🤓(nerd-face)",
"😎(smiling-face-with-sunglasses)",
"🥸(disguised-face)",
"🥳(partying-face)",
"😵‍💫(face-with-spiral-eyes)",
"🫩(face-with-bags-under-eyes)",
"👍(thumbs-up)",
"👎(thumbs-down)",
"👋(waving-hand)",
"🤚(raised-back-of-hand)",
"🖐(hand-with-fingers-splayed)",
"🖖(vulcan-salute)",
"👌(ok-hand)",
"🤌(pinched-fingers)",
"🤏(pinching-hand)",
"✌️(victory-hand)",
"🤞(crossed-fingers)",
"🤟(love-you-gesture)",
"🤘(sign-of-the-horns)",
"🤙(call-me-hand)",
"👈(pointing-left)",
"👉(pointing-right)",
"👆(pointing-up)",
"👇(pointing-down)",
"🫵(pointing-at-the-viewer)",
"🫆(fingerprint)",
"🐶(dog)",
"🐱(cat)",
"🐭(mouse)",
"🐹(hamster)",
"🐰(rabbit)",
"🦊(fox)",
"🐻(bear)",
"🐼(panda)",
"🐻‍❄️(polar-bear)",
"🐨(koala)",
"🐯(tiger)",
"🦁(lion)",
"🐮(cow)",
"🐷(pig)",
"🐸(frog)",
"🐵(monkey)",
"🐥(baby-chick)",
"🐢(turtle)",
"🐳(spouting-whale)",
"🐬(dolphin)",
"🪾(leafless-tree)",
"🍎(apple)",
"🍐(pear)",
"🍊(tangerine)",
"🍋(lemon)",
"🍌(banana)",
"🍉(watermelon)",
"🍇(grapes)",
"🍓(strawberry)",
"🫐(blueberries)",
"🍈(melon)",
"🍒(cherries)",
"🍑(peach)",
"🥭(mango)",
"🍍(pineapple)",
"🥑(avocado)",
"🍆(eggplant)",
"🥔(potato)",
"🥕(carrot)",
"🌽(corn)",
"🌶️(hot-pepper)",
"🫜(root-vegetable)",
"🍕(pizza)",
"🍔(hamburger)",
"🍟(french-fries)",
"🍣(sushi)",
"🍦(soft-serve)"]
INTERVAL = 300  # 5 Minutes

st.set_page_config(page_title="Emoji Identity Sync", page_icon="🛡️")

st.title("🛡️ Secure Emoji Identity Sync")
st.write("A decentralized way to verify identity using timed emoji sequences.")

# --- 3. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    room_name = st.text_input("Private Room Name", value="General", help="Both devices must match.")
with col2:
    ssn_input = st.text_input("Enter ID Number", type="password", placeholder="000-00-0000")

# --- 4. LOGIC ---
if ssn_input and room_name:
    # Handle the Global Counter
    # We use 'session_state' to ensure a refresh doesn't count as a new entry
    if 'already_counted' not in st.session_state:
        ticker["count"] += 1
        st.session_state.already_counted = True

    # Time-based Hash Logic
    current_time = time.time()
    time_block = int(current_time // INTERVAL)
    seconds_remaining = INTERVAL - int(current_time % INTERVAL)
    
    # Secure Hashing (Using a local salt for this version)
    salt = "LocalSecret2026" 
    combined = f"{ssn_input}{salt}{time_block}{room_name.lower().strip()}"
    hash_hex = hashlib.sha256(combined.encode()).hexdigest()
    
    # Map Hash to Emojis
    idx1 = int(hash_hex[0:8], 16) % len(EMOJI_POOL)
    idx2 = int(hash_hex[8:16], 16) % len(EMOJI_POOL)
    idx3 = int(hash_hex[16:24], 16) % len(EMOJI_POOL)

    # --- 5. UI DISPLAY ---
    st.divider()
    
    # Display the Global Ticker
    st.metric(label="Total Generator Uses (Across All Users)", value=ticker["count"])
    
    st.write(f"### Current Identity for Room: `{room_name}`")
    st.title(f"{EMOJI_POOL[idx1]} {EMOJI_POOL[idx2]} {EMOJI_POOL[idx3]}")
    
    # Visual Countdown
    progress = seconds_remaining / INTERVAL
    st.progress(progress, text=f"Sequence rotates in {seconds_remaining // 60}m {seconds_remaining % 60}s")
    
    # Auto-refresh helper
    time.sleep(1)
    st.rerun()

else:
    st.warning("Please enter both a Room Name and an ID Number to generate your sequence.")
    # Show current global count even when idle
    st.sidebar.metric("Global Usage", ticker["count"])
    
