import streamlit as st
import hashlib
import time

# Configuration
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
INTERVAL = 300  # 5 minutes in seconds

st.title("🛡️ Identity Emoji Verifier")
st.write("Enter your ID to see your current 5-minute security sequence.")

# User Input
ssn_input = st.text_input("Enter Social Security Number", type="password", placeholder="000-00-0000")

if ssn_input:
    # Logic for Time-Based Rotation
    current_time = time.time()
    time_block = int(current_time // INTERVAL)
    seconds_remaining = INTERVAL - int(current_time % INTERVAL)
    
    # Secure Hashing
    salt = "SecretProject2026"
    combined = f"{ssn_input.replace('-', '')}{salt}{time_block}"
    hash_hex = hashlib.sha256(combined.encode()).hexdigest()
    
    # Map to 3 Emojis
    idx1 = int(hash_hex[0:8], 16) % len(EMOJI_POOL)
    idx2 = int(hash_hex[8:16], 16) % len(EMOJI_POOL)
    idx3 = int(hash_hex[16:24], 16) % len(EMOJI_POOL)
    
    # Display Result
    st.subheader("Your Identity Sequence:")
    st.code(f"{EMOJI_POOL[idx1]} {EMOJI_POOL[idx2]} {EMOJI_POOL[idx3]}", language="")
    
    # Countdown Timer
    st.info(f"This sequence will rotate in {seconds_remaining // 60}m {seconds_remaining % 60}s")
    
    # Force refresh when timer hits zero
    time.sleep(1)
    st.rerun()
