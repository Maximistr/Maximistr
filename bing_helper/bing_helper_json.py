import pyautogui
import time
import random
import json
import subprocess
import os

# ───────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────

SEARCHES_TO_DO = 35
PHRASES_FILE = "phrases.json"          # ← must be in the same folder

MIN_DELAY = 15
MAX_DELAY = 30

# ───────────────────────────────────────────────

# Load phrases from JSON file
try:
    with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
        phrases = json.load(f)
    if not phrases:
        raise ValueError("No phrases found in JSON file!")
    print(f"Loaded {len(phrases)} phrases from {PHRASES_FILE}")
except FileNotFoundError:
    print(f"Error: {PHRASES_FILE} not found in the same folder!")
    exit(1)
except Exception as e:
    print(f"Error loading JSON: {e}")
    exit(1)

def human_like_mouse_jiggle():
    """Very subtle mouse movements — stays roughly over/near the search bar"""
    try:
        # Get starting position so we can stay close to it
        start_x, start_y = pyautogui.position()
    except:
        return  # skip if can't get position

    for _ in range(random.randint(3, 8)):   # more frequent but tiny moves
        # Very small offsets — almost unnoticeable but looks more natural
        x_offset = random.randint(-10, 10)
        y_offset = random.randint(-8, 8)

        # Keep it very close to original position
        pyautogui.moveRel(x_offset, y_offset, duration=0.08 + random.uniform(0, 0.12))
        time.sleep(random.uniform(0.07, 0.20))  # brief pauses between micro-moves
    
    # Return to starting point
    pyautogui.moveTo(start_x, start_y, duration=0.5)

print(f"Will perform {SEARCHES_TO_DO} searches using {len(phrases)} loaded phrases.")
print("  • Press Ctrl+C in this window to stop early")
print("\nOpening Bing.com in Edge...\n")

subprocess.Popen(["C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "https://www.bing.com/search?q=."])
time.sleep(1)  # Wait for Edge to open and load Bing
pyautogui.moveTo(278, 155)  # Move mouse to Bing search box area
time.sleep(1)

print("Starting in 8 seconds...\n")

time.sleep(8)

try:
    for i in range(SEARCHES_TO_DO):
        # Choose random phrase
        phrase = random.choice(phrases)
        
        pyautogui.click()  # ensure search box is active (sometimes needed)
        time.sleep(0.12 + random.uniform(0, 0.20))
        
        # Select all text in the search box
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.12 + random.uniform(0, 0.20))


        # Type the phrase slowly (human-like typing speed)
        pyautogui.write(phrase, interval=random.uniform(0.04, 0.11))
        time.sleep(0.25 + random.uniform(0, 0.35))

        # Submit search
        pyautogui.press('enter')
        print(f"[{i+1:2d}/{SEARCHES_TO_DO}] → {phrase}")

        # ~60-70% chance of very subtle mouse movement
        if random.random() < 0.68:
            human_like_mouse_jiggle()

        # Realistic random delay between searches
        wait_time = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"    → waiting {wait_time} seconds...")
        time.sleep(wait_time)

    print("\nAll searches completed.")
    print("closing the window.\n")
    os.system("taskkill /f /im msedge.exe")

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C pressed).")
except Exception as e:
    print(f"\nUnexpected error: {e}")
