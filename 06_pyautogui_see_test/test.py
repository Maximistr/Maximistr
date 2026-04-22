import pyautogui as pag
import pygetwindow as gw
import time


cell_dis = 16
cell_width = 16
cell_height = 16
start_cell = 0
mines = 40
flag_count = 0
name = "Max"

blank = (192,192,192)
one = (0,0,255)
two = (0, 128, 0)
three = (255,0,0)
four = (0,0,128)
five = (128,0,0)
six = (0,128,128)
eight = (192,192,192)
flag = (0,0,0)

rows = []
changes = 0
hi_num = 0
streak = False
streak_num = None
no_streak = 0
loose_streak = False
time.sleep(2)
window = gw.getWindowsWithTitle('Minesweeper')[0]
window.restore()
window.activate()
region = (window.left, window.top, window.width, window.height)

pag.moveTo(region[0] + 23, region[1] + 109)
print(region[0])
print(region[1])
print(pag.position())
start_cell = pag.position()
start_time = time.time()
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
                        rows[target[pos][0]][target[pos][1]] = match_color((x, y))
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


def match_color(pos):
        global streak
        global hi_num
        global streak_num
        color = pag.pixel(pos[0], pos[1])
        match color:
            case c if c == blank:
                if streak == True:
                    num = streak_num
                else:
                    new_col = pag.pixel(pos[0] - 7, pos[1])
                    if new_col == (255,255,255):
                        num = "C"
                        streak_num = "C"
                    else:
                        num = 0
                        streak_num = 0
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
            case c if c == six:
                num = 6
                streak = False
            case c if c == eight:
                num = 8
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
    for x in range(cell_height):
        field = []
        streak = False
        for y in range(cell_width):
            scanned_pixel_x =  start_cell.x + cell_dis * y
            scanned_pixel_y = start_cell.y + cell_dis * x
            col = match_color((scanned_pixel_x, scanned_pixel_y))
            field.append(col)
        
        print(field)
        rows.append(field.copy())


while flag_count != mines:
    for x in range(1,hi_num+1):
        check(x)
    if changes == 0 and loose_streak == False:
        rows = []
        check_screen()
        loose_streak = True
    elif changes == 0 and loose_streak == True:
        print("You have to guess now, good luck! :)")
        quit()
    elif changes > 0:
        loose_streak = False
    changes = 0
for r in range(len(rows)):
        for c in range(len(rows[r])):
            print(f"Checking cell [{r}][{c}] = {rows[r][c]}")
            if rows[r][c] == "C":
                x = start_cell.x + cell_dis * c
                y = start_cell.y + cell_dis * r
                pag.moveTo(x,y)
                pag.click()
                rows[r][c] = match_color((x,y))
        
for row in rows:
    print(' '.join(str(x).center(3) for x in row))
end_time = time.time()
total_time = end_time - start_time
print(f"Time taken: {total_time:.2f} seconds")
print("Done!")
