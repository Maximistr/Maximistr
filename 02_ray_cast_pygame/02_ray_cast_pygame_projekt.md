# Raycasting 3D Game Engine (Ray Cast Pygame)

## Popis a cíl projektu
Cílem je vytvořit interaktivní 3D herní engine v 2D prostředí pygame pomocí raycasting algoritmu. Aplikace umožňuje hráči procházet 2D mapou a vizualizovat ji jako 3D prostředí z pohledu hráče. Hra je plně funkční akční hra s vícenásobným systémem úrovní, nepřáteli, municí, sbíránímu předmětů a efekty.

## Hlavní Features
- **Raycasting 3D engine**: Odsílání paprsků z pozice hráče do mapy k detekci zdí
- **3D renderer**: Vykreslování stěn na obrazovku na základě vzdálenosti
- **Systém úrovní**: 5 progresivních úrovní s rostoucí obtížností
- **Nepřátelé**: AI nepřátelé s patrolováním a pronásledováním hráče
- **Systém municí**: 3 kulatnice za úroveň s automatickým dobíjením (1,5s na jednu kulku)
- **Sbírání předmětů**: Mince rozptýlené po mapě (více na vyšších úrovních)
- **Efekty**: Částicové efekty při smrti nepřátel, fade-out animace
- **Zdraví hráče**: Zdravotní systém s vizuální indikací
- **Scoring systém**: Skóre za zabití nepřátel a sbírání mincí
- **Minimap**: Živá minimapu s pozicí hráče a nepřátel

## Herní Mechaniky

### Úrovně (Levels)
- **Úroveň 1**: 3 nepřátelé, 5 mincí, normální obtížnost
- **Úroveň 2**: 5 nepřátel, 6 mincí, zvýšené health a rychlost
- **Úroveň 3**: 7 nepřátel, 7 mincí, další zvýšení
- **Úroveň 4**: 9 nepřátel, 8 mincí, vysoká obtížnost
- **Úroveň 5**: 11 nepřátel, 9 mincí, extrémní obtížnost

**Obtížnost škálování:**
- Zdraví nepřátel zvyšuje se 1,3x za úroveň
- Rychlost nepřátel +15% za úroveň
- Zdraví hráče +20% per úroveň

### Ammo Systém
- Start: 3 kulatnice za úroveň
- Nabíjení: 1,5 sekund na jednu kulku
- Automaticky se nabíjí bez akce hráče
- Střelba NE-resetuje dobíjecí čas (progresivní náboj)
- Vizuální indikátor: Ammo bar a reload progress %

### Nepřátelé (Enemies)
- **AI**: Pronásledují hráče při viditelnosti
- **Zdraví**: 50 HP (škálované úrovní)
- **Poškození**: Způsobují 0.1 HP damage za tick při dotyku
- **Znovu spawn**: Ne (jednou přemoženi = pryč)

### Předměty (Items)
- **Mince**: +10 skóre za sbírku
- **Dynamické spawnování**: Počet se zvyšuje s úrovní
- **Cíl úrovně**: Musíte sebrat VŠECHNY mince NEBO porazit všechny nepřátele

### Efekty
- **Částicové efekty**: 15 částic při smrti nepřátel
- **Fade-out**: Částice postupně mizí (30 frames)
- **Barva**: Orange-red explose efekt
- **3D rendering**: Částice jsou vykresleny v 3D prostoru

## Ovládání
- **W/A/S/D**: Pohyb a strafe
- **MYŠÍ**: Pohled (FPS styl)
- **SPACE/Klik myší**: Střelba
- **M**: Otevřít menu výběru úrovně
- **ESC**: Ukončit hru

## Technická část

### Použité knihovny
- **pygame**: Grafika a event handling
- **math**: Matematické výpočty (sinus, kosinus, atan2, sqrt)
- **sys**: Systémové funkce
- **random**: Generování map a pozic

### Algoritmy

**Raycasting algoritmus (DDA - Digital Differential Analyzer)**:
1. Z pozice hráče se odesílá série paprsků rovnoměrně rozprostřených v zorném poli
2. Pro každý paprsek se zjistí jeho průsečík se zdí v mapě
3. Vzdálenost průsečíku určuje výšku vykreslené stěny (fish-eye korrekce)
4. Barva se upravuje podle vzdálenosti

**Generování map**:
- Procedurální generování herny se místnostmi a chodbami
- 15 místností náhodné velikosti
- Spojení místností koridory (spojitý prostor)

**AI Nepřátel**:
- Path finding: Pohyb směrem k hráči (jednoduché vektorové přiblížení)
- Collision: Skluzu po zdích (X a Y osy testují zvlášť)

**Systém částic**:
- Vytváření: 15 částic na náhodné úhly s náhodnou rychlostí
- Aktualizace: Pohyb a fade-out animace
- Vykreslování: 3D projekce s hloubkovým efektem

### Datové struktury
```python
player = {
    'x': float,           # Pozice X
    'y': float,           # Pozice Y
    'angle': float,       # Úhel rotace (radiány)
    'speed': float,       # Rychlost pohybu
    'health': float,      # Zdraví hráče
    'ammo': int,          # Aktuální munice
    'max_ammo': int,      # Maximální munice
    'reload_start_time': int or None  # Čas spuštění nabíjení
}

enemy = {
    'x': float,           # Pozice X
    'y': float,           # Pozice Y
    'health': float,      # Zdraví nepřítele
    'speed': float,       # Rychlost pohybu
    'anim_offset': int    # Offset animace
}

fireball = {
    'x': float,           # Pozice X
    'y': float,           # Pozice Y
    'angle': float,       # Úhel letu
    'speed': float,       # Rychlost
    'distance': float     # Uražená vzdálenost
}

particle = {
    'x': float,           # Pozice X
    'y': float,           # Pozice Y
    'angle': float,       # Úhel pohybu
    'speed': float,       # Rychlost pohybu
    'life': int,          # Zbývající životní bod
    'max_life': int,      # Maximální život
    'color': tuple        # RGB barva
}
```

### Grafické nastavení
- **Rozlišení**: 1200x600
- **FOV**: 60 stupňů (π/3 radiánů)
- **Počet paprsků**: 80
- **Maximální vzdálenost**: 20 jednotek
- **FPS**: 60 (vsync není)

### Optimalizace
- Počet paprsků lze regulovat (více = vyšší kvalita, nižší FPS)
- Caching stínování pro stěny
- Efektivní collision detection

## Herní stavy (Game States)
1. **Úvodní menu**: Výběr úrovně
2. **Gameplay**: Aktivní hraní úrovně
3. **Úroveň Hotová**: Úspěšný konec úrovně
4. **Game Over**: Smrt hráče
5. **Celková skóre**: Přehled progrese

## Budoucí Vylepšení
- Zvuk a hudba
- Další typy nepřátel (ranged, tank)
- Power-ups (zdraví, zesílení)
- Různé typy zbraní
- Leaderboard
- Settings menu
- More visual effects (screen shake, blood)
