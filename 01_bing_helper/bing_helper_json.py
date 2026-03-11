import subprocess
import sys
def ensure_module_installed(module_name, package_name=None):
    """
    Check if a module is installed, and install it if not.
    
    Args:
        module_name: The name used in import statements
        package_name: The pip package name (if different from module_name)
    """
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name} is already installed")
    except ImportError:
        print(f"✗ {package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ {package_name} installed successfully")
# Ensure required modules are installed
print("Checking required modules...\n")
ensure_module_installed("pyautogui")
# Now import all modules
import pyautogui
import time
import random
import json
import os

# ───────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────

SEARCHES_TO_DO = 35
PHRASES_FILE = "phrases.json"          # ← must be in the same folder
SEARCH_BOX_COORDS = 278, 155              # Coordinates of Bing search box (x, y), use test.py to find yours

MIN_DELAY = 15
MAX_DELAY = 30

used_phrases = []
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
    """
    Funkce pro velmi jemné pohyby myší (simulace lidského faktoru).
    Zvyšuje důvěryhodnost bota tím, že neudržuje myš zcela nehybně.
    """
    try:
        # Získání výchozí pozice, abychom se k ní mohli na konci vrátit
        start_x, start_y = pyautogui.position()
    except:
        return  # Přerušení, pokud pozici nelze zjistit

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
pyautogui.moveTo(SEARCH_BOX_COORDS)  # Move mouse to Bing search box area
time.sleep(1)

print("Starting in 8 seconds...\n")

time.sleep(8)

try:
    for i in range(SEARCHES_TO_DO):
        # 1. Výběr náhodného vyhledávacího dotazu ze seznamu 'phrases'
        phrase = random.choice(phrases)
        while phrase in used_phrases:
            phrase = random.choice(phrases)
        used_phrases.append(phrase)
        
        # 2. Aktivace vyhledávacího pole kliknutím a krátké posečkání
        pyautogui.click()
        time.sleep(0.12 + random.uniform(0, 0.20))
        
        # 3. Vybrání případného předchozího textu (Ctrl+A)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.12 + random.uniform(0, 0.20))


        # 4. Manuální vložení textu po jednotlivých znacích
        # Rychlost je mírně náhodná pro simulaci psaní člověkem
        pyautogui.write(phrase, interval=random.uniform(0.04, 0.11))
        time.sleep(0.25 + random.uniform(0, 0.35))

        # 5. Odeslání požadavku klávesou Enter
        pyautogui.press('enter')
        print(f"[{i+1:2d}/{SEARCHES_TO_DO}] → {phrase}")

        # 6. Náhodný pohyb myší: s šancí zhruba 68 % pohne myší na pozadí (simuluje čtení výsledků)
        if random.random() < 0.68:
            human_like_mouse_jiggle()

        # 7. Časové okno pro prodlevu mezi hledáními
        # Slouží k prevenci odhalení bota kvůli příliš rychlým a pravidelným dotazům
        wait_time = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"    → waiting {wait_time} seconds...")
        time.sleep(wait_time)

    print("\nAll searches completed.")
    print("closing the window.\n")
    os.system("taskkill /f /im msedge.exe")

except KeyboardInterrupt:
    print("\nStopped by user (Ctrl+C pressed).")
except ModuleNotFoundError:
    print("\nModuleNotFoundError: Please install the required modules.")
except Exception as e:
    print(f"\nUnexpected error: {e}")
