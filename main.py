import pygame as pg
import random
from pygame.locals import *
import numpy as np

pg.init()

def wait_for_click():
    while True:
        for event in pg.event.get():
            try:
                if event.type==MOUSEBUTTONDOWN:
                    return event.button
            except KeyboardInterrupt:
                return

def get_pose(board, size_squares):
    event = wait_for_click()
    x, y = pg.mouse.get_pos()
    return int(np.floor(x / size_squares)), int(np.floor(y / size_squares)), event

def clearing(pos, cleared, board):
    difficulties = {
        'beginner': (8, 8),
        'intermediate': (16, 16),
        'expert': (30, 16)
    }
    i, j = difficulties[difficulty]
    x, y = pos
    if not board[y][x].isnumeric():
        for w in range(3):
            for v in range(3):
                if (x+w-1, y+v-1)!=(x, y):
                    X=x+w-1
                    Y=y+v-1
                    try:
                        if (X, Y) not in cleared and (i-1)>=X>=0 and 0<=Y<=(j-1):
                            cleared.add((X, Y))
                            if board[Y][X]==' ' or not (w, v)!=(0, 0) and (w, v)!=(2, 2) and (w, v)!=(0, 2) and (w, v)!=(2, 0):
                                clearing((X, Y), cleared, board)
                    except IndexError:
                        pass

def create_board(difficulty):
    board = []
    difficulties = {
        'beginner': (8, 8, 10),
        'intermediate': (16, 16, 40),
        'expert': (30, 16, 99)
    }
    i, j, bombs = difficulties[difficulty]
# making the empty board
    for y in range(j):
        row = []
        for x in range(i):
            row.append(' ')
        board.append(row)
# setting random bombs (x, y)
    bomb_arr = []
    while len(bomb_arr)<bombs:
        pos = (random.randint(0, i-1), random.randint(0, j-1))
        if pos not in bomb_arr:
            bomb_arr.append(pos)
# putting bombs on board
    for pos in bomb_arr:
        x, y = pos
        board[y][x]='B'
# filling in the rest
    for x, y in bomb_arr:
            for w in range(3):
                for v in range(3):
                    if (x+w-1, y+v-1)!=(x, y):
                        X=x+w-1
                        Y=y+v-1
                        if (i-1)>=X>=0 and 0<=Y<=(j-1):
                            if board[Y][X]==' ':
                                board[Y][X]='1'
                            elif board[Y][X].isnumeric() and int(board[Y][X])>=1:
                                board[Y][X] = str(eval(f'{board[Y][X]}+1'))
    return board

flag = []
clicked = set()
def turn(board, difficulty):
    sizes = {
        'beginner': (8, 8, 100, 10),
        'intermediate': (16, 16, 50, 40),
        'expert': (30, 16, 50, 99)
    }
    i, j, size, bombs = sizes[difficulty]
    x, y, event = get_pose(board, size)
    if event==1:
        if (x,y) not in flag:
            if board[y][x]=='B':
                return 0
            elif board[y][x]==' ':
                clicked.add((x, y))
                clearing((x, y), clicked, board)
            else:
                clicked.add((x, y))
            if (i*j-len(clicked))==bombs:
                return 1
    if event==3:
        if (x, y) not in flag:
            flag.append((x, y))
        else:
            flag.remove((x, y))
    print_board(window, difficulty, clicked, flag)
    return 2

def set_text(string, coord_x, coord_y, font, font_size, color):
    font = pg.font.SysFont(font, font_size)
    text = font.render(string, True, color)
    text_rect = text.get_rect()
    text_rect.center = (coord_x, coord_y)
    return text, text_rect

def print_board(window, difficulty, arr, flag):
    dark_gray = (169, 169, 169)
    darker_gray = (70, 70, 70)
    light_gray = (211, 211, 211)
    red = (255, 0, 0)
    difficulties = {
        'beginner': (8, 8, 1),
        'intermediate': (16, 16, 2),
        'expert': (30, 16, 2)
    }

    i, j, s = difficulties[difficulty]
    for y in range(1, j+1):
        for x in range(1, i+1):
            if (x-1, y-1) in flag:
                text = set_text('f', (50+100*(x-1))/s, (50+100*(y-1))/s, "Comic Sans MS", 50, red)
                window.blit(text[0], text[1])
            elif (x-1, y-1) in arr:
                pg.draw.rect(window, light_gray, [100*(x-1)/s, 100*(y-1)/s, 100/s, 100/s])
                text = set_text(board[y-1][x-1], (50+100*(x-1))/s, (50+100*(y-1))/s, "Comic Sans MS", 50, (0, 150, 0))
                window.blit(text[0], text[1])
            else:
                pg.draw.rect(window, dark_gray, [100*(x-1)/s, 100*(y-1)/s, 100/s, 100/s])
                pg.draw.rect(window, darker_gray, [(10+100*(x-1))/s, (10+100*(y-1))/s, 80/s, 80/s])
    pg.display.update()

difficulty = input()
resolutions = {
    'beginner': (800, 800),
    'intermediate': (800, 800),
    'expert': (1500, 800)
}
window_width, window_height = resolutions[difficulty]
window = pg.display.set_mode((window_width, window_height))
board = create_board(difficulty)
print_board(window, difficulty, [], flag)
win = False
while True:
    val = turn(board, difficulty)
    if val==1:
        print('wiener')
        break
    elif val==0:
        print('exploded')
        break
