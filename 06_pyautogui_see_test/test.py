import pyautogui as pag
import pynput
import pygetwindow as gw
import json

cell_dis = 16
cell_width = 16
cell_height = 16  
start_cell = 0
mines = 40
flag_count = 0

blank = (192,192,192)
one = (0,0,255)
two = (0, 128, 0)
three = (255,0,0)
four = (0,0,128)
five = (128,0,0)
flag = (0,0,0)

rows = []
changes = 0
hi_num = 0
streak = False
streak_num = None
no_streak = 0

window = gw.getWindowsWithTitle('Minesweeper')[0]
window.restore()
window.activate()
region = (window.left, window.top, window.width, window.height)

pag.moveTo(region[0]+23, region[1]+120)
print(region[0])
print(region[1])
print(pag.position())
start_cell = pag.position()
pag.click()

def check(number):
    global flag_count
    global changes
    global mines
    for r in range(len(rows)):
        for c in range(len(rows[r])):
            print(f"Checking cell [{r}][{c}] = {rows[r][c]}")
            if rows[r][c] == number:
                print(f"  Found {number} at [{r}][{c}]")
                target =  []
                flags = 0
                for dr in range(-1,2):
                    for dc in range(-1,2):
                        nr = r + dr
                        nc = c + dc

                        if 0 <= nr < len(rows) and 0 <= nc < len(rows[r]):
                            if rows[nr][nc] == "C":
                                target.append((nr, nc))
                            if rows[nr][nc] == "F":
                                flags += 1
                print(f"  Temp count: {len(target)}")
                print(f"{flags} flags around")
                if flags == number:
                    for pos in range(len(target)):
                        x = start_cell.x + cell_dis * target[pos][1]
                        y = start_cell.y + cell_dis * target[pos][0]
                        pag.moveTo(x,y)
                        pag.click()
                        rows[target[pos][0]][target[pos][1]] = match_color()
                        changes += 1
                elif len(target) + flags == number:
                    for p in range(len(target)):
                        tr = target[p][0]
                        tc = target[p][1]
                        rows[tr][tc] = "F"
                        print(f"  Temp == 1! Flagging [{tr}][{tc}]")
                        x = start_cell.x + cell_dis * tc
                        y = start_cell.y + cell_dis * tr

                        pag.moveTo(x, y)
                        print(f"  Moved to: ({x}, {y})")
                        pag.rightClick()
                        flag_count += 1
                        changes += 1


def match_color():
        global streak
        global hi_num
        global streak_num
        color = pag.pixel(pag.position().x, pag.position().y)
        match color:
            case c if c == blank:
                if streak == True:
                    num = streak_num
                else:
                    pag.moveRel(-7,0)
                    new_col = pag.pixel(pag.position().x, pag.position().y)
                    if new_col == (255,255,255):
                        num = "C"
                        streak_num = "C"
                    else:
                        num = 0
                        streak_num = 0
                    pag.moveRel(7,0)
                streak = True
            case c if c == one:
                num = 1
                streak = False
            case c if c == two:
                num = 2
                streak = False
            case c if c == three:
                num = 3
                streak = False
            case c if c == four:
                num = 4
                streak = False
            case c if c == five:
                num = 5
                streak = False        
            case c if c == flag:
                num = "F"
                streak = False
            case _:
                num = "idk"
                print(c)
        if isinstance(num, int) and num > hi_num:
            hi_num = num
        return num

def check_screen():
    global streak
    pag.moveTo(start_cell)
    for x in range(cell_height):
        field = []
        streak = False
        for y in range(cell_width):

            col = match_color()
            field.append(col)
            
            pag.moveRel(cell_dis, 0)
        
        print(field)
        rows.append(field.copy())

        pag.moveRel(-cell_dis*cell_width, cell_dis)

while flag_count != mines:
    for x in range(1,hi_num+1):
        check(x)
    if changes == 0:
        rows = []
        check_screen()
    changes = 0
        
for row in rows:
    print(' '.join(str(x).center(3) for x in row))
