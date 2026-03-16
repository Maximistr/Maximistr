# Raycasting 3D Game Engine (Ray Cast Pygame)

## Popis a cíl projektu
Cílem je vytvořit interactive 3D herní engine v 2D prostředí pygame pomocí raycasting algoritmu. Aplikace umožňuje hráči procházet 2D mapou a vizualizovat ji jako 3D prostředí z pohledu hráče. Hra je určena pro demonstraci grafických principů raycasting techniky.

## Funkcionalita programu
- **Raycasting engine**: Odesílání paprsků z pozice hráče do mapy k detekci zdí
- **3D renderer**: Vykreslování stěn na obrazovku na základě vzdálenosti zachycené paprsky
- **Player movement**: Pohyb hráče pomocí WASD nebo šipek
- **Map system**: Dvourozměrná mapa reprezentovaná 2D polem (0 = volné místo, 1 = zeď)
- **Real-time rendering**: Dynamické vykreslování scény v reálném čase

## Technická část

### Použité knihovny
- **pygame**: Grafika a event handling
- **math**: Matematické výpočty (sinus, kosinus, atan2)
- **sys**: Systémové funkce

### Algoritmy a princip
**Raycasting algoritmus**:
1. Z pozice hráče se odesílá série paprsků rovnoměrně rozprostřených kolem jeho zorného pole
2. Pro každý paprsek se zjistí jeho průsečík se zdí v mapě
3. Vzdálenost průsečíku určuje výšku vykreslené stěny na obrazovce
4. Barva se upravuje podle vzdálenosti (mlžitý efekt)

**Výpočet paprsku**:
- Paprsek: počáteční bod (x, y hráče) + směr (úhel)
- Grid collision: Testování průsečíku s buňkami mapy

### Datové struktury
- **game_map**: 2D pole reprezentující mapu (seznam seznamů)
- **player**: Slovník obsahující x, y pozici a úhel rotace
- **Raycast result**: Výstup obsahující vzdálenost a typ stěny

### Implementační detaily
- Fixed aspect ratio zobrazení pro konzistentní vzhled
- Optimalizace: Počet paprsků lze regulovat (více paprsků = vyšší kvalita, nižší FPS)
- Normal mapping: Rozlišení mezi vertikálními a horizontálními zdmi (různé barvy)
