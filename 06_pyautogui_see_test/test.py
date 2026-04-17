import pyautogui as pag
import pynput
import pygetwindow as gw
# set cell size and the distance from each other
cell_dis = 20
cell_width = 9
cell_height = 9
# set the colors of the numbers
blank = (192,192,192)
one = (0,0,255)
two = (0, 128, 0)
three = (255,0,0)

field = []
#prepare the minesweeper window
window = gw.getWindowsWithTitle('Minesweeper')[0]
window.restore()
window.activate()
region = (window.left, window.top, window.width, window.height)

pag.moveTo(region[0]+30, region[1]+136)
print(pag.position())
pag.click()
for x in range(cell_height):
    for y in range(cell_width):
        color = pag.pixel(pag.position().x,pag.position().y)
        match color:
            case c if c == blank:
                field.append("0")    
            case c if c == one:
                field.append("1")
            case c if c == two:
                field.append("2")
            case c if c == three:
                field.append("3")
            case _:
                field.append("idk")
                print(c)
        pag.moveRel(cell_dis,0)
    print(field)
    field = []
    pag.moveRel(-cell_dis*cell_width,cell_dis)

