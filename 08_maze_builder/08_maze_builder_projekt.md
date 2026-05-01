# Maze Builder - Generátor a Vizualizér Bludišť

## Popis a cíl projektu

Aplikace slouží k automatickému generování náhodných bludišť pomocí algoritmu rekurzivního prohledávání (Recursive Backtracking). Program umožňuje vytvářet bludiště různých velikostí, vizualizovat je v terminálu, exportovat do textového formátu a hledat cestu z bludiště pomocí algoritmu BFS (Breadth-First Search). Aplikace je určena pro studijní a edukační účely, demonstruje práci s datovými strukturami (matice, fronty, zásobníky) a prohledávacími algoritmy.

## Funkcionalita programu

- **Generování bludišť**: Použití algoritmu rekurzivního prohledávání k vytvoření náhodného bludiště
- **Vizualizace v terminálu**: Zobrazení bludiště pomocí ASCII znaků (# pro stěny, space pro chodby)
- **Hledání cesty**: Algoritmus BFS pro nalezení nejkratší cesty z počátečního bodu do cíle
- **Export a import**: Ukládání a načítání bludišť ze souborů
- **Konfigurovatelné rozměry**: Uživatel může zadat velikost bludiště
- **Měření času**: Sledování doby generování a hledání řešení

## Technické detaily

**Použité knihovny:**
- `random` - pro náhodné volby při generování
- `time` - pro měření výkonu
- `json` - pro ukládání a načítání dat

**Algoritmy:**
- Recursive Backtracking - pro generování bludiště
- Breadth-First Search (BFS) - pro hledání cesty

**Datové struktury:**
- 2D pole (matice) - reprezentace bludiště
- Queue (fronta) - pro BFS algoritmus
- Stack (zásobník) - pro rekurzivní generování
