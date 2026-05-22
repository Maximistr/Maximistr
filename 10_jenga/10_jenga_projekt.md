# Jenga 3D Izometrická Krychle

## Popis a cíl projektu
Tento projekt vytváří jednoduchou izometrickou 3D vizualizaci krychle pomocí knihovny `pygame`. Aplikace je určena pro studenty, kteří se učí principy 3D projekce, rotace v prostoru a vykreslování pomocí 2D grafiky.

Cílem je předvést, jak převést 3D souřadnice na 2D obrazovku, jak natočit objekt kolem všech tří os a jak vykreslit pouze viditelné stěny pomocí zjednodušeného algoritmu cullingu.

## Funkcionalita programu
- Otevření okna s rozlišením 800 × 600 pixelů.
- Vykreslení krychle ve 3D prostoru, která se do výsledného snímku převádí izometrickou projekcí.
- Interaktivní ovládání rotace krychle pomocí kláves:
  - `←` / `→` – rotace kolem osy Y
  - `↑` / `↓` – rotace kolem osy X
  - `A` / `D` – rotace kolem osy Z
- Barevné odlišení jednotlivých stěn krychle a černý obrys pro lepší čitelnost.
- Zobrazení pouze orientovaných stěn, které jsou viditelné divákovi.

## Technická část
- Použité knihovny:
  - `pygame` pro otevření okna, správu vstupu a vykreslování polygonů.
  - `math` pro výpočty funkcí `sin` a `cos` při rotacích.
- Algoritmy a postupy:
  - Izometrická projekce: 3D body se převedou na 2D pomocí pevných kosinusových a sinusových koeficientů.
  - 3D rotace: postupné otáčení bodů kolem os X, Y a Z pomocí standardních rotačních matic.
  - Backface culling: určení, zda je stěna krychle natočená směrem k divákovi, výpočtem orientovaného obsahu v 2D.
- Datové struktury:
  - Seznam 3D rohů krychle jako osmička tuple hodnot `(x, y, z)`.
  - Seznam stěn jako indexy rohů, které tvoří polygon.
- Struktura programu:
  - `project(x, y, z)`: převede 3D bod na 2D obrazovku.
  - `rotate_point(x, y, z, ax, ay, az)`: otočí bod kolem zadaných os.
  - `draw_cube(surface, angle_x, angle_y, angle_z)`: vytvoří rotované body, provede projekci a vykreslí stěny.
  - `main()`: inicializuje Pygame, zpracovává události, aktualizuje rotaci a přepočítává snímky.

## Obsah dokumentace
- Název projektu: Jenga 3D Izometrická Krychle
- Popis a cíl projektu: viz výše
- Popis funkcionality programu: vykreslení rotující krychle, ovládání, projekce a culling.
- Technická část: knihovny, algoritmy, datové struktury, funkční rozdělení.
