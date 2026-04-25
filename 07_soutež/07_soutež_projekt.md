# Hra s kostkami - Kniffel

## Popis a cíl projektu
Aplikace implementuje hru s šesti kostkami (obdobu hry Kniffel/Yahtzee). Hra je určena pro 2-4 hráče, kteří se střídají v tazích a snaží se dosáhnout co nejvyšího skóre vyplňováním různých kategorií. Cílem je edukativní projekt na procvičení OOP v Pythonu a logiky herního systému.

## Funkcionalita programu

### Hlavní funkce:
- **Vytvoření hráčů**: Hra支持 2-4 hráče, každý má své jméno
- **Házení kostkami**: Standardní hod 6 kostkami (hodnoty 1-6)
- **Přeházení kostky**: Hráč může dvakrát během tahu vybrat kostky k přeházení
- **Bodovací kategorie**:
  - Základní čísla (1-6): Součet všech kostek s daným číslem
  - Malé (1-3): Součet kostek s čísly 1, 2, 3
  - Velké (4-6): Součet kostek s čísly 4, 5, 6
  - Sudé: Součet všech sudých kostek
  - Liché: Součet všech lichých kostek
  - Dvoják: Tři stejné kostky
  - Troják: Dvě dvojice (např. 2,2,3,3,5)
  - Generál: Všech 6 stejných kostek
  - Postupka: Všechny kostky s různými čísly (1,2,3,4,5,6)
  - Pyramida: Kombinace trojáku a páru (např. 3,3,3,2,2)
- **Bodování**: Hráč vyplní jednu kategorii po každém tahu
- **Konec hry**: Hra končí, když hráč vyplní všech 15 kategorií

### Technická část

**Použité prvky:**
- **Datové struktury**:
  - Třída `player_class`: Uchovává informace o hráči (jméno, body, kategorie)
  - Slovník `numbers_cat`: Tracking používaných základních kategorií (1-6)
  - Seznamy: Sledování dostupných kategorií a jejich stavů
- **Algoritmy**:
  - Analytika kostek: Počítání výskytů každého čísla
  - Validace kategorií: Kontrola, zda je kombinace kostek vhodná pro danou kategorii
  - Logika bodování: Výpočet bodů podle zvoleného typu kategorie
- **Standardní knihovny**:
  - `random`: Generování náhodných hodnot pro házení kostkami
- **Klíčové funkce**:
  - `turn(player)`: Řídí celý tah hráče (hod, přeházení, výběr kategorie, bodování)
  - `availible_categories()`: Zobrazuje dostupné kategorie a aktuální skóre
  - `basic_numbers()`: Přiděluje body za základní čísla
  - `add_points()`: Přiděluje body za speciální kategorie

**Herní smyčka:**
- Hra pokračuje, dokud poslední hráč nevyplní všech 15 kategorií
- Hráči se střídají v tazích
- Po každém tahu se zobrazí stav kategorií a bodů
