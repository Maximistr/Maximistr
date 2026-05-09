# Maze Builder - Generátor a Vizualizér Bludišť

## Popis a cíl projektu

Aplikace slouží k automatickému generování náhodných bludišť pomocí algoritmu rekurzivního prohledávání (Recursive Backtracking). Program umožňuje vytvářet bludiště různých velikostí, vizualizovat je v terminálu, exportovat do textového formátu a hledat cestu z bludiště pomocí algoritmu BFS (Breadth-First Search). Aplikace je určena pro studijní a edukační účely, demonstruje práci s datovými strukturami (matice, fronty, zásobníky) a prohledávacími algoritmy.

## Funkcionalita programu

- **Generování bludišť**: Použití algoritmu rekurzivního prohledávání k vytvoření náhodného bludiště
- **Grafické rozhraní (GUI)**: Interaktivní okno s vizualizací bludiště pomocí barevných pixelů
- **Interaktivní hra**: Hráč se pohybuje skrz bludiště pomocí klávesnice
- **Hledání cesty**: Algoritmus BFS pro nalezení nejkratší cesty z počátečního bodu do cíle
- **Export a import**: Ukládání a načítání bludišť ze souborů
- **Konfigurovatelné rozměry**: Uživatel může zadat velikost bludiště
- **Měření času**: Sledování doby generování a hledání řešení
- **Win detection**: Detekce dosažení cíle a gratulace hráči

## Technické detaily

**Použité knihovny:**
- `tkinter` - pro vytvoření grafického rozhraní
- `random` - pro náhodné volby při generování
- `time` - pro měření výkonu
- `json` - pro ukládání a načítání dat
- `collections.deque` - pro BFS algoritmus

**Algoritmy:**
- Recursive Backtracking - pro generování bludiště
- Breadth-First Search (BFS) - pro hledání cesty

**Datové struktury:**
- 2D pole (matice) - reprezentace bludiště
- Queue (fronta) - pro BFS algoritmus
- Stack (zásobník) - pro rekurzivní generování

## Ovládání

**Pohyb v bludišti:**
- **W / ↑** - Pohyb nahoru
- **S / ↓** - Pohyb dolů
- **A / ←** - Pohyb doleva
- **D / →** - Pohyb doprava
- **R** - Resetování pozice na start

**Tlačítka v rozhraní:**
- **Generovat** - Vytvoření nového bludiště (zadání šířky a výšky)
- **Najít cestu** - Zobrazení optimální cesty (žlutou barvou)
- **Vyčistit** - Odstranění zobrazené cesty
- **Resetovat hru** - Vrácení hráče na start
- **Uložit** - Uložení bludiště do JSON souboru
- **Načíst** - Načtení bludiště z JSON souboru

## Barvy v GUI

- **🟩 Zelená** - Startovní pozice
- **🟥 Červená** - Cíl (konec bludiště)
- **🔵 Cyan** - Pozice hráče
- **🟨 Žlutá** - Optimální cesta (když je zobrazena)
- **⬛ Tmavě šedá** - Stěny
- **⬜ Bílá** - Chodby
