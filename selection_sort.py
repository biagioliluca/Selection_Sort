import pygame as pg # https://www.pygame.org/docs/
import sys
import pygame_gui as pgui # https://pygame-gui.readthedocs.io/en/latest/index.html
import random

'''
Program to visualize Selection Sort algorithm
This program could present some bugs: can't draw some rectangles at fast while loop speed
'''

HEIGHT = 720
WIDTH = 1280
C_HEIGHT = 680
C_WIDTH = 990
RECT_WIDTH = 5
FPS = 1000

rects = []
values = []
active_rect :tuple = None
clock :pg.time.Clock = None
screen :pg.Surface = None
canvas :pg.Surface = None
ui_manager :pgui.UIManager = None
button :pgui.elements.UIButton = None


def fill_canvas():
    global canvas
    x0 = 1
    parameter = 4
    for value in values:
        rect_height = value*parameter
        rects.append(pg.draw.rect(canvas, (255,255,255), pg.Rect(x0,C_HEIGHT-rect_height, RECT_WIDTH, rect_height)))
        x0 += RECT_WIDTH+1
        
def init_gui():
    global clock, button, ui_manager, screen, canvas
    pg.init() # initilize all the imported pygame modules
    pg.display.set_caption('Search Algorithms')
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    screen.fill((0,0,0))
    ui_manager = pgui.UIManager((WIDTH, HEIGHT))
    button = pgui.elements.UIButton(relative_rect=pg.Rect((1098, 500), (100, 40)),
                                        text='Start',
                                        manager=ui_manager)
    canvas = pg.Surface((C_WIDTH, C_HEIGHT))
    canvas.fill((100,100,100))
    fill_canvas()
    screen.blit(canvas, dest = (20,20)) # displays canvas and all its inner elements
    # pg.display.flip()

def init_logic():
    global values
    values = [value for value in range(1,166)]
    random.shuffle(values)

def initialize():
    init_logic()
    init_gui()

def swap_rects(i, j):
    global rects
    i_left = rects[i].left
    i_top = rects[i].top
    i_height = rects[i].height

    j_left = rects[j].left
    j_top = rects[j].top
    j_height = rects[j].height

    del rects[i]
    rects.insert(i, pg.draw.rect(canvas, (0,0,0), pg.Rect(i_left, j_top, RECT_WIDTH, j_height)))

    del rects[j]
    rects.insert(j, pg.draw.rect(canvas, (0,0,0), pg.Rect(j_left, i_top, RECT_WIDTH, i_height))) 
    
def color_rectangle(idx):
    global rects, canvas, active_rect, screen
    left = rects[idx].left
    top = rects[idx].top
    height = rects[idx].height

    if active_rect == None:     
        del rects[idx]
        rects.insert(idx, pg.draw.rect(canvas, 'red', pg.Rect(left, top, RECT_WIDTH, height)))
        active_rect = (rects[idx], idx)
    else:
        # redraw old active rect with white color
        a_left = active_rect[0].left
        a_top = active_rect[0].top
        a_height = active_rect[0].height

        del rects[active_rect[1]]
        rects.insert(active_rect[1], pg.draw.rect(canvas, (255,255,255), pg.Rect(a_left, a_top, RECT_WIDTH, a_height)))


        del rects[idx]
        rects.insert(idx, pg.draw.rect(canvas, 'red', pg.Rect(left, top, RECT_WIDTH, height)))
        active_rect = (rects[idx], idx)

    screen.blit(canvas, dest = (20,20))

def reload():
    canvas.fill((100,100,100))
    for idx in range(len(rects)):
        left = rects[idx].left
        top = rects[idx].top
        height = rects[idx].height

        del rects[idx]
        rects.insert(idx, pg.draw.rect(canvas, (255,255,255), pg.Rect(left, top, RECT_WIDTH, height)))

    screen.blit(canvas, dest = (20,20))

out_index = 0
in_index = 0
min = out_index
start = False

if __name__ == '__main__':
    initialize()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit() # opposite of init
                sys.exit() # not strictly needed, it shuts down the game
            
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    start = True
            ui_manager.process_events(event)

        if start:
            if out_index != len(values):
                in_index += 1
                if in_index == len(values):
                    values[out_index], values[min] = values[min], values[out_index]
                    swap_rects(out_index, min)
                    reload()
                    out_index += 1
                    min = out_index
                    in_index = out_index
                else:
                    color_rectangle(in_index)
                    if values[in_index] < values[min]:
                        min = in_index
            else:
                start = False
                out_index = 0
                in_index = 0
                min = out_index
                print(values)

        deltatime = clock.tick(FPS)/1000.0 # set the FPS (how many times the while loop per sec) and return the ms passed each frame, we divide 1000 to get seconds       
        ui_manager.update(deltatime)
        # pg.display.update()
        ui_manager.draw_ui(screen)
        pg.display.flip() # it draws whatever was pinted in the loop cicle (it refresh the screen with new data)
        



