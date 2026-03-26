# Brawl Stars API Projekt

## Popis a cíl projektu
Aplikace slouží k interakci s Brawl Stars API pro získávání dat o hráčích, týmech a jejich statistikách. Cílem je vytvořit nástroj pro analýzu herních dat a zobrazení relevantních informací o hráčích a jejich pokroku v hře.

## Funkcionalita programu
- Vyhledávání hráčů podle jména nebo tagu
- Získávání statistik hráčů (úroveň, trofeje, vítězství/porážky)
- Načítání informací o klubech
- Ukládání a srovnávání dat hráčů
- Bezpečné uložení API klíče pomocí proměnných prostředí (.env soubor)
- Práce s REST API pomocí requests knihovny
- Zpracování JSON dat z API

## Technická část
- **Jazyk**: Python 3.x
- **Knihovny**: requests (HTTP komunikace), python-dotenv (správa proměnných prostředí), json
- **API**: Brawl Stars Official API (https://brawlstars.fandom.com/wiki/API)
- **Bezpečnost**: API token uložen v .env souboru (ne v kódu)
