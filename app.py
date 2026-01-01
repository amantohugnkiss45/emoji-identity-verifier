import streamlit as st
import hashlib
import time

# --- Configuration ---
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
INTERVAL = 300 # 5 Minutes

st.set_page_config(page_title="Emoji Sync Pro", page_icon="🛡️")

st.title("🛡️ Secure Emoji Sync")
st.info("To sync two devices, ensure both enter the same Room Name and ID.")

# --- Private Session Inputs ---
col1, col2 = st.columns(2)
with col1:
    room_name = st.text_input("Private Room Name", value="Session-1", help="Both devices must use the same room name.")
with col2:
    ssn_input = st.text_input("Enter ID Number", type="password", placeholder="000-00-0000")

if ssn_input and room_name:
    # 1. Time Calculation
    current_time = time.time()
    time_block = int(current_time // INTERVAL)
    seconds_remaining = INTERVAL - int(current_time % INTERVAL)
    
    # 2. Secure Hash with Room Isolation
    # We pull the SALT from Streamlit Secrets for real security
    salt = st.secrets.get("SECRET_SALT", "DefaultLocalSalt123")
    combined = f"{ssn_input.replace('-', '')}{salt}{time_block}{room_name.lower().strip()}"
    hash_hex = hashlib.sha256(combined.encode()).hexdigest()
    
    # 3. Generate Triple Sequence
    idx1 = int(hash_hex[0:8], 16) % len(EMOJI_POOL)
    idx2 = int(hash_hex[8:16], 16) % len(EMOJI_POOL)
    idx3 = int(hash_hex[16:24], 16) % len(EMOJI_POOL)
    
    # --- UI Display ---
    st.divider()
    st.write(f"### Current Verification Code for Room: `{room_name}`")
    st.title(f"{EMOJI_POOL[idx1]} {EMOJI_POOL[idx2]} {EMOJI_POOL[idx3]}")
    
    # Progress bar to show time remaining in the current block
    progress = seconds_remaining / INTERVAL
    st.progress(progress, text=f"Rotating in {seconds_remaining // 60}m {seconds_remaining % 60}s")
    
    # Auto-refresh the page
    time.sleep(1)
    st.rerun()
    
