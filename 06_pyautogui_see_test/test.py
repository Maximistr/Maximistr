import pyautogui as pag
import pynput
import pygetwindow as gw

# Konfigurace hracího pole - nastavení rozměrů a mezer
cell_dis = 20          # Vzdálenost mezi jednotlivými buňkami v pixelech
cell_width = 9         # Počet sloupců (buněk v řádku)
cell_height = 9        # Počet řádků (buněk v sloupci)
start_cell = 0

# Mapování RGB barev na stavy buněk
# Barvy jsou určeny podle vizuálního vzhledu Minesweeper aplikace
blank = (192,192,192)  # Prázdná buňka (šedá)
one = (0,0,255)        # Buňka s jednou sousedující minou (modrá)
two = (0, 128, 0)      # Buňka se dvěma sousedícími minami (zelená)
three = (255,0,0)      # Buňka se třemi sousedícími minami (červená)

# Inicializace seznamu pro ukládání dat řádku

rows = []

# Lokalizace a příprava okna Minesweeper aplikace
# Vyhledání okna podle názvu a uvedení do popředí
window = gw.getWindowsWithTitle('Minesweeper')[0]
window.restore()           # Obnovení normální velikosti okna
window.activate()          # Aktivace okna do popředí
region = (window.left, window.top, window.width, window.height)

# Nastavení počáteční pozice kurzoru na prvopou buňku hracího pole
# Offsety (30, 136) jsou zjištěny empiricky pro standardní Minesweeper
pag.moveTo(region[0]+30, region[1]+136)
print(pag.position())
start_cell = pag.position()
pag.click()  # Kliknutí na herní desku aktivuje herní okno

# Hlavní smyčka pro zpracování hracího pole
# Vnější smyčka - iterace po řádcích (délka: cell_height = 9)
for x in range(cell_height):
    field = []
    # Vnitřní smyčka - iterace po sloupcích (délka: cell_width = 9)
    for y in range(cell_width):
        # Přečtení RGB barvy aktuálního pixelu pod kurzorem
        color = pag.pixel(pag.position().x, pag.position().y)
        
        # Porovnání přečtené barvy s definovanými stavy pomocí match-case
        # Mapování: barva -> hodnota buňky
        match color:
            case c if c == blank:
                pag.moveRel(-10,0)
                new_col = pag.pixel(pag.position().x, pag.position().y)
                if new_col == (255,255,255):
                    field.append("C")  #nevíme co je
                else:
                    field.append(0)   #Sousedství s nula minami
                pag.moveRel(10,0)
            case c if c == one:
                field.append(1)    # Sousedství s jednou minou
            case c if c == two:
                field.append(2)    # Sousedství se dvěma minami
            case c if c == three:
                field.append(3)    # Sousedství se třemi minami
            case _:
                field.append("idk")  # Neznámá barva - nelze klasifikovat
                print(c)              # Výpis neznámé barvy pro DEBUG
        
        # Pohyb kurzoru o jednu buňku doprava (cell_dis pixelů)
        pag.moveRel(cell_dis, 0)
    
    # Tisk výsledků pro aktuální řádek
    print(field)
    rows.append(field.copy())
    # Reset seznamu pro příští řádek

    
    # Pohyb na začátek dalšího řádku: vlevo (cell_dis*cell_width) a dolů (cell_dis)
    pag.moveRel(-cell_dis*cell_width, cell_dis)

for r in range(len(rows)):
    for c in range(len(rows[r])):
        print(f"Checking cell [{r}][{c}] = {rows[r][c]}")
        if rows[r][c] == 1:
            print(f"  Found 1 at [{r}][{c}]")
            temp = 0
            target = None
            for dr in range(-1,2):
                for dc in range(-1,2):
                    nr = r + dr
                    nc = c + dc
                    # ---- EDGE CHECK ----
                    if 0 <= nr < len(rows) and 0 <= nc < len(rows[r]):
                        if rows[nr][nc] == "C":
                            temp += 1
                            target = (nr, nc)
            print(f"  Temp count: {temp}")
            if temp == 1 and target:
                rows[tr][tc] = "F"
                tr, tc = target
                print(f"  Temp == 1! Flagging [{tr}][{tc}]")
                x = start_cell.x + cell_dis * tc
                y = start_cell.y + cell_dis * tr

                pag.moveTo(x, y)
                print(f"  Moved to: ({x}, {y})")
                pag.rightClick()