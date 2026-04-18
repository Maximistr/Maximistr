# Minesweeper Board Reader

## Popis a cíl projektu

Cílem projektu je vytvořit automatizovaný nástroj, který dokáže číst a analyzovat stav herní desky v aplikaci Minesweeper. Program pomocí počítačového vidění (pixel detection) identifikuje obsah jednotlivých buněk a vytváří digitální reprezentaci herní desky. Aplikace je určena pro porozumění principům automatizace desktopových aplikací a základům obrazové analýzy.

## Funkcionalita programu

### Technické prvky

- **Knihovny:** 
  - `pyautogui` - pro kontrolu pozice myši a čtení barev pixelů
  - `pynput` - pro práci s vstupními zařízeními
  - `pygetwindow` - pro správu oken aplikací

- **Funkční principy:**
  - Lokalizace okna Minesweeper aplikace v systému
  - Navigace po hracím poli pomocí relativního pohybu myši
  - Detekce barev jednotlivých buněk
  - Mapování barev na číselné hodnoty (0 = prázdné, 1-3 = počty sousedících min)
  - Sběr dat do 2D reprezentace herní desky

- **Datové struktury:**
  - 1D seznam `field` pro ukládání stavu buněk během zpracování řádku
  - Textové reprezentace stavů buněk ("0", "1", "2", "3", "idk")

- **Algoritmus:**
  1. Najde a aktivuje okno Minesweeper
  2. Iniciálně zacílí na první buňku hracího pole
  3. Iterativně prochází pole řádek po řádku
  4. Pro každou buňku přečte RGB hodnotu pixelu
  5. Porovnáním s přednastavenými barvami určí obsah buňky
  6. Ukládá výsledky do seznamu a vypisuje řádky

- **Konfigurace:**
  - `cell_dis` = vzdálenost mezi buňkami (pixels)
  - `cell_width` = počet buněk v řádku (9)
  - `cell_height` = počet buněk v sloupci (9)
  - Hardkodované barvy pro jednotlivé stavy buněk

### Omezení a závislosti

- Program vyžaduje spuštěnou aplikaci Minesweeper
- Rozlišení a vizuální vzhled Minesweeper musí odpovídat přednastavenému nastavení barev
- Pozice okna se musí nacházet v očekávané poloze na obrazovce
