# Interaktivní Systém Částic s Fyzikou

## Popis a cíl projektu
Aplikace je interaktivní fyzikální simulátor částic v reálném čase. Uživatel může interaktivně spouštět částice do prostoru, které se řídí zákony klasické fyziky - gravitace, odpor vzduchu, elastické srážky. Cílem je demonstrovat realističkou fyzikální simulaci s vizuálním zpětným vazebám a umožnit uživateli experimentovat s různými fysikálními jevy.

## Funkcionalita programu
- **Generování částic**: Uživatel kliknutím vytváří částice v náhodných barvách
- **Gravitační pole**: Všechny částice jsou ovlivněny gravitací směrem dolů
- **Fyzika částic**: Pohyb, akcelerace, tření, odpor vzduchu
- **Kolize**: Elastické srážky částic mezi sebou a se stěnami
- **Interaktivní ovládání**: 
  - LMB (levé kliknutí) - spuštění částic
  - RMB (pravé kliknutí) - přitažlivá síla (magnet)
  - SPACE - vybuchnutí všech částic (rozpraší je)
  - C - vyčistit všechny částice
- **Vizuální efekty**: Částice se kreslí s barvou odpovídající jejich energii, stopy za pohybem

## Technická část
- **Knihovny**: pygame (grafika, события), math (trigonometrie, fyzika)
- **Algoritmy**: Euler integrátor pro simulaci, prostorové dělení pro detekci kolizí
- **Datové struktury**: Třída Particle s vlastnostmi (pozice, rychlost, zrychlení, barva)
- **Fyzika**: 
  - Gravitace: F = mg (g = 9.81)
  - Odpor: F_drag = -c * v
  - Elastické srážky: Zachování hybnosti a energie
  - Detekce kolizí: Vzdálenost středů < součet poloměrů
