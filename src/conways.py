import pygame, sys, random, copy
from pygame.locals import *

pygame.init()
BLOCK_SIZE = BLOCK_W, BLOCK_H = (8, 8)
BLOCKS = BLOCKS_COLS, BLOCKS_ROWS = 80,80
size = width, height = (BLOCK_W * BLOCKS[0], BLOCK_H * BLOCKS[1])
screen = pygame.display.set_mode(size)
# pygame.display.set_caption("Conway's Game of Life")
pygame.display.set_caption('Space Bar = Pause/Resume * R key = Reset * Left click while paused will place a cell')
MARGIN = 3
SQ_LENGTH = 10
SQ_NUM = 49 # min squares per row/column is 15
WIN_SIZE = (SQ_NUM+1)*MARGIN + SQ_NUM*SQ_LENGTH
BTN_SIZE = 30
generations = 0
running = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

BLACK = (  0,   0,   0)
RED= (200, 0, 0 )
GRAY = (25, 25, 25)

class Grid:
    paused = False

    def __init__(self, screen):
        self.screen = screen
        self.cells = []
        for _ in range(BLOCKS_COLS):
            cell = [False] * BLOCKS_ROWS
            self.cells.append(cell)
        self.randomize()

    def randomize(self):
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                if random.choice([True, False]):
                    self.cells[x][y] = True

    def toggle_pause(self):
        self.paused = not self.paused

    def click_at(self, point):
        if self.paused:
            x, y = point
            block_x, block_y = x // BLOCK_W, y // BLOCK_H
            self.cells[block_x][block_y] = not self.cells[block_x][block_y]

    def draw_grid(self):
        BLUISH = (30, 30, 100)
        for i in range(BLOCKS_COLS):
            start_point = (i * BLOCK_W, 0)
            end_point = (i * BLOCK_W, height)
            pygame.draw.line(self.screen, BLUISH, start_point, end_point, 1)
        for i in range(BLOCKS_ROWS):
            start_point = (0, i * BLOCK_H)
            end_point = (width, i * BLOCK_H)
            pygame.draw.line(self.screen, BLUISH, start_point, end_point, 1)

    def draw_cells(self):
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                if self.cells[x][y]:
                    x2, y2 = x * BLOCK_W, y * BLOCK_H
                    cell = pygame.Rect([x2+1, y2+1, BLOCK_W-1, BLOCK_H-1])
                    pygame.draw.rect(self.screen, RED, cell)

    def border_at(self, point):
        borders = 0
        x, y = point
        points = ((x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y),
                  (x-1, y-1), (x, y-1), (x+1, y-1))
        for x2, y2 in points:
            try:
                if 0 <= x2 < BLOCKS_COLS and 0 <= y2 < BLOCKS_ROWS:
                    if self.cells[x2][y2]:
                        borders += 1
                else:
                    continue
            except IndexError:
                pass
        return borders

    def step(self):
        if self.paused:
            return
        cells = copy.deepcopy(self.cells)
        for x in range(BLOCKS_COLS):
            for y in range(BLOCKS_ROWS):
                borders = self.border_at((x, y))
                if not self.cells[x][y]:
                    if borders == 3:
                        cells[x][y] = True
                elif self.cells[x][y]:
                    if not 2 <= borders <= 3:
                        cells[x][y] = False
        self.cells = cells

# Declare some buttons
font = pygame.font.Font('freesansbold.ttf', 16) 

inc_time_step_button = pygame.draw.rect(screen, (175, 203, 255), pygame.Rect(10,WIN_SIZE+10,3*BTN_SIZE, BTN_SIZE))
dec_time_step_button = pygame.draw.rect(screen, (175, 203, 255), pygame.Rect(20+3*BTN_SIZE,WIN_SIZE+10,3*BTN_SIZE, BTN_SIZE))
stop_play_button = pygame.draw.rect(screen, (175, 203, 255), pygame.Rect(30+6*BTN_SIZE,WIN_SIZE+10,3*BTN_SIZE, BTN_SIZE))
restart_button = pygame.draw.rect(screen, (175, 203, 255), pygame.Rect(40+9*BTN_SIZE,WIN_SIZE+10,3*BTN_SIZE, BTN_SIZE))
generation_display = pygame.draw.rect(screen, GRAY, pygame.Rect(60+12*BTN_SIZE,WIN_SIZE+10,3*BTN_SIZE, BTN_SIZE))


grid = Grid(screen)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                grid.toggle_pause()
            elif event.key == K_r:
                grid.randomize()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid.click_at(pygame.mouse.get_pos())

    screen.fill(BLACK)
    grid.draw_grid()
    grid.draw_cells()
    clock.tick(5)
    pygame.display.flip()
    grid.step()