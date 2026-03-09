# Bing Rewards Automation Project

Tento dokument vychází z požadavků na projekt a spojuje dřívější podrobnou dokumentaci do předepsaného formátu.

## Popis a cíl projektu
This is a Python automation project that demonstrates how to build a bot to automatically perform Bing searches. The project showcases skills in automation, user interface interaction, browser integration, and scripting.

**Project Goals:**
- Learn Python automation libraries (`pyautogui`, `subprocess`)
- Understand browser automation and keyboard/mouse control
- Implement human-like behavior patterns (random delays, mouse movements)
- Work with JSON data files
- Create batch files for easy execution
- Practice GitHub version control and documentation

## Funkcionalita programu
Program je plně automatizovaný skript fungující nad systémem Windows, který otevírá prohlížeč s Bingem a nasimuluje chování uživatele vyhledávajícího dotazy, a to za použití různých externích knihoven a JSON souborů jako databází dotazů. 

### Technická část
- **Python 3.13** - Main programming language.
- **pyautogui** - Použito pro manipulaci s myší a klávesnicí. Obsahuje implementaci na "mouse jiggling" drobných, náhodných pohybů myší simulující reálného uživatele (od -10 do +10 pixelů).
- **subprocess** - Otevírání browseru (např. *Edge*).
- **json** - Data file handling, ze souboru `phrases.json` s více než 400 vyhledávacími frázemi, dělené do různých kategorií. Program je navržen s ohledem na *Separation of concerns* (data uložena odděleně od logiky).
- **Náhodnost (randomizace)** - Algoritmy pro random delay (15-30s) a náhodnou rychlost psaní (0.04-0.11 sekundy per znak). Tímto program minimalizuje opakující se strojový pattern a anti-bot obranu.

### Project Structure (Soubory)
```
01_bing_helper/
│ 01_bing_helper_projekt.md # Tento dokument
│ bing_helper_json.py     # Main automation script (obsahuje auto-install wrapper modulů)
│ phrases.json            # Search phrases database
│ run_bing.bat            # Windows batch runner
│ coordinates_find.py     # Interaktivní myšový tool pro hledání souřadnic na monitoru
```

### Automation Logic Flow (Algoritmus pro vyhledávání)
The core logic performs these steps for each search:
1. Click the search box
2. Select all text (Ctrl+A)
3. Type a random phrase slowly (human-like typing)
4. Press Enter to search
5. Wait a random duration (15-30 seconds)
6. Optionally jiggle the mouse around (68% chance)
7. Vše se opakuje pro nadefinovaný počet cyklů (`SEARCHES_TO_DO`).

### How to Use This Project

1. **Install dependencies (automatic):**
   The scripts now automatically install required modules on first run (`ensure_module_installed()`). No manual `pip install` needed!

2. **Configure your phrases** - Edit `phrases.json` with your search terms (now includes 400+ phrases)

3. **Find your search box coordinates:**
   - Run `python coordinates_find.py`
   - Click on the Bing search box, note the coordinates printed.
   - Middle-click to exit the tool.
   - Update `SEARCH_BOX_COORDS` in `bing_helper_json.py`.

4. **Run the script:**
   - Option A: Double-click `run_bing.bat`
   - Option B: Run `python bing_helper_json.py`

5. **Watch it work** - The script handles everything automatically for ~13 minutes (for 30 searches).

### Challenges & Solutions (Výzvy a úskalí při implementaci)
- **Finding the search box location**: Vytvořen separátní nástroj `coordinates_find.py` pomáhající uživateli kliknout a ihned získat X.Y pozici.
- **Script running too fast / looking robotic**: Implementovány delaye 15-30 s.
- **Edge not launching**: Změněno na explicitní PATH (`C:\Program Files (x86)\...`).
- **Ease of execution**: Zapsáno do spustitelného .bat failu - jednoklikový start na Windows.

---
**Note:** This project is for educational purposes only to understand automation concepts.
