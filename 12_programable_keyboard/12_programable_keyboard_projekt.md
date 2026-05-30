# VMacropad Manager

## Popis a cíl projektu
VMacropad Manager je GUI aplikace pro programování a správu programovatelné klávesnice/makropadu s USB HID podporou. Aplikace umožňuje uživatelům vytvářet a spravovat různé předvolby (presety) s vlastními kombinacemi kláves, mediálních ovládání, akcí myši a LED režimů. Aplikace také automaticky přepíná mezi presety na základě aktivní aplikace či okna v systému. Projekt je určen pro práci s hardwarem s konkrétními USB VID/PID identifikátory.

## Funkcionalita programu

### Hlavní funkce:
- **Správa Presetů**: Uživatel může vytvářet, ukládat, načítat a mazat presety s různými konfiguracijami
- **Konfigurace Tlačítek (6x)**: Nastavení každého z 6 tlačítek na:
  - Klávesové zkratky s modifikátory (Ctrl, Shift, Alt, Win)
  - Mediální ovládání (Play/Pause, Next, Mute, Vol Up/Down, atd.)
  - Akce myši (levé/pravé kliknutí, kolečko, vpřed/vzad)
- **Konfigurace Otočného Kóderu**: 3 akce - otáčení proti směru hodinových ručiček (CCW), otáčení po směru (CW), stisknutí
- **LED Režimy**: Ovládání LED osvětlení (vypnuto, statické, dýchající)
- **Automatické Přepínání Presetů**: 
  - Přepínání podle aktivní aplikace (process name)
  - Přepínání podle názvů oken (s podporou regex)
  - Výchozí preset pro aplikace bez mapování
- **Vizualizace Hardwaru**: Interaktivní 2D vizualizace makropadu pro výběr tlačítek
- **Pokročilé Nastavení**:
  - Vlastní USB VID/PID nastavení
  - Notifikace při změnách presetů
  - Integrace do systémové lišty (tray icon)
  - Spuštění s Windows
  - Automatické aktualizace z GitHub

### Technická část

**Použité Knihovny:**
- `tkinter` + `customtkinter (ctk)`: GUI framework pro moderní tmavý interface
- `hidapi (hid)`: USB HID komunikace s hardwarem
- `psutil`, `pywin32`: Detekce aktivní aplikace a okna (Windows-specific)
- `PIL (Pillow)`: Tvorba tray ikony
- `pystray`: Integrace systémové lišty
- `json`: Ukládání a načítání konfigurací
- `threading`: Asynchronní komunikace s hardwarem a monitorování aplikací
- `webbrowser`, `urllib`: Správa updatů a GitHub API

**Datové Struktury:**
- `Theme`: Třída s konstantami barev pro UI
- `MacroPadDevice`: Třída spravující USB HID komunikaci se zařízením
- `VMacroApp`: Hlavní GUI aplikace (dědí z `ctk.CTk`)
- Slovníky pro mapování: `KEY_MAP`, `MEDIA_MAP`, `MOUSE_BUTTONS`, `MOUSE_WHEEL`, `LED_MODES`
- `current_data`: Pole 9 prvků (6 tlačítek + 3 otočného kodéru) se stavem každé akce
- `presets`: Slovník uložených presetů s jejich konfiguracemi
- `app_mappings`: Mapování aplikací a názvů oken na presety

**Klíčové Algoritmy:**
- **Detekce Hardwaru**: Skenování USB zařízení podle VID/PID, hledání správného HID interface
- **USB Komunikace**: Strategie pro zápis dat (output vs feature report), s fallback mechanismem
- **Monitorování Oken**: Cihlová smyčka (každých 1s) detekující změny aktivního okna s debounce
- **Auto-switching Logika**: Prioritizace (názvů oken > aplikace > default), s zamykáním po manuální volbě
- **Vizualizace**: 2D kreslení makropadu s detektováním kliku na jednotlivá tlačítka
- **Ukládání Konfigurací**: JSON persistence presetů, mapování a nastavení

**Řešené Problémy:**
- Hardware Omezení: Emulace Back/Forward tlačítek myši přes Media Control kvůli firmware limitaci
- CustomTkinter Bug: Bezpečná oprava mouse wheel eventu pro Combobox
- Dependencies: Fallback při chybění psutil/pywin32 (auto-switching vypnut)
- Multi-Threading: Zamykací mechanismy pro bezpečný přístup k datům z více vláken
- UI Responsiveness: Asynchronní komunikace s hardwarem, aby neusnula UI

**Herní/Aplikační Smyčky:**
- `check_conn_loop()`: Monitoruje spojení s hardwarem (interval 2s)
- `app_monitor_loop()`: Detekuje změny aktivního okna a automaticky přepíná presety (interval 1s)
- `perform_initial_connection()`: Pokus o spojení s hardwarem při startu aplikace
- Hlavní GUI smyčka: `mainloop()` pro zpracování uživatelských akcí

**Uživatelské Profily:**
- Tray mode: Aplikace běží na pozadí v systémové liště
- Full mode: Aplikace viditelná v okně
- Auto-update: Kontrola nových verzí z GitHub (jen pro PyInstaller balíčky)
