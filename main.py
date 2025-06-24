import pygame
import random
import math
import time
from operator import add, sub

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACKGROUND_COLOR = (70, 130, 130)
SNAKE_COLOR = (0, 255, 255)

FPS = 4
MSPF = (1/FPS)*1000

EMPTY_SPACE = 0
SNAKE_HEAD = 1
SNAKE_TAIL = 2
APPLE = 3

# Directions
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Screen dimensions
GRID_STEPS = 29
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH
SCREEN_HEIGHT = GRID_STEPS * GRID_HEIGHT

class Grid:
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)

    snakeDir: tuple = LEFT
    snakePos = (0, 0)
    snakeTail = list()

    applePos = (0, 0)
    
    def __init__(self) -> None:
        self._game_over = False
        random.seed
        self.snakePos = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        (taili, tailj) = tuple(map(sub, self.snakePos, self.snakeDir))
        self.snakeTail.append((taili,tailj))

        (i, j) = self.snakePos
        self.set_item(i, j, SNAKE_HEAD)
        self.set_item(i, j, SNAKE_TAIL)

        self.new_apple()

    def new_apple(self):
        self.applePos = (applei, applej) = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        self.set_item(applei, applej, APPLE)

    def get_item(self, i, j):
        return self.grid[j*GRID_WIDTH + i]
    
    def set_item(self, i, j, item):
        self.grid[j*GRID_WIDTH + i] = item
    
    def clear_grid(self):
        self.grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)

    def update_grid(self):
        (i, j) = self.snakePos
        self.set_item(i, j, SNAKE_HEAD)

        for (i, j) in self.snakeTail:
            self.set_item(i, j, SNAKE_TAIL)

        (i, j) = self.applePos
        self.set_item(i, j, APPLE)

    def tick(self):
        (nexti, nextj) = tuple(map(add, self.snakePos, self.snakeDir))

        if(nexti < 0):
            nexti = GRID_WIDTH-1
        if(nextj < 0):
            nextj = GRID_WIDTH-1
        if(nexti > GRID_WIDTH-1):
            nexti = 0
        if(nextj > GRID_HEIGHT-1):
            nextj = 0

        if(self.get_item(nexti, nextj) == EMPTY_SPACE):
                self.snakeTail = list(self.snakeTail[:-1])
                self.snakeTail.insert(0, self.snakePos)
                self.snakePos = (nexti, nextj)       
        elif(self.get_item(nexti, nextj) == APPLE):
                self.snakeTail.insert(0, self.snakePos)
                self.snakePos = (nexti, nextj)
                self.new_apple()
        elif(self.get_item(nexti, nextj) == SNAKE_TAIL):
                self._game_over = True

        self.clear_grid()
        self.update_grid()

class App:
    grid = Grid()

    def __init__(self):
        self._running = True
        #self._display_surf = None
        self.size = self.weight, self.height = SCREEN_WIDTH, SCREEN_HEIGHT

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.SHOWN)
        self._running = True
        self._step = False
        self._tick = False
        self._pause = False
        self._last_tick = 0

        

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_SPACE):
                self._pause = not self._pause
            if(self._tick == True):
                if(event.key == pygame.K_UP and self.grid.snakeDir != DOWN):
                    self.grid.snakeDir = UP
                    pygame.display.set_caption("UP")
                if(event.key == pygame.K_DOWN and self.grid.snakeDir != UP):
                    self.grid.snakeDir = DOWN
                    pygame.display.set_caption("DOWN")
                if(event.key == pygame.K_LEFT and self.grid.snakeDir != RIGHT):
                    self.grid.snakeDir = LEFT
                    pygame.display.set_caption("LEFT")
                if(event.key == pygame.K_RIGHT and self.grid.snakeDir != LEFT):
                    self.grid.snakeDir = RIGHT
                    pygame.display.set_caption("RIGHT")
                self._tick = False

    def on_loop(self):
        self.grid.tick()

    def on_render(self):
        self._display_surf.fill(pygame.Color(BACKGROUND_COLOR))
        self.draw_grid()
        pygame.display.flip()

    def draw_shape(self, i, j):
        if(self.grid.get_item(i,j) == SNAKE_HEAD):
            center = (i*GRID_STEPS + GRID_STEPS/2, j*GRID_STEPS + GRID_STEPS/2)
            pygame.draw.circle(self._display_surf,
                            SNAKE_COLOR,
                            center,
                            GRID_STEPS/2,)
            
        elif(self.grid.get_item(i, j) == SNAKE_TAIL):
            pygame.draw.rect(self._display_surf, pygame.Color(255,255,255),
                                    pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS),
                                    0)
        elif(self.grid.get_item(i,j) == APPLE):
            center = (i*GRID_STEPS + GRID_STEPS/2, j*GRID_STEPS + GRID_STEPS/2)
            pygame.draw.circle(self._display_surf,
                            RED,
                            center,
                            GRID_STEPS/2,)
        elif(self.grid.get_item(i, j) == EMPTY_SPACE):
            pygame.draw.rect(self._display_surf, pygame.Color(0,200,150),
                                    pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS),
                                             1)
            
    def draw_grid(self):
        for j in range(0, GRID_HEIGHT):
            for i in range(0, GRID_WIDTH):
                self.draw_shape(i, j)
                
    

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            ticks = pygame.time.get_ticks()
            if((ticks - self._last_tick > MSPF) and not self._pause and not self.grid._game_over):
                self._tick = True
                self._last_tick = ticks
                self.on_loop()
                self.on_render()
            else:
                time.sleep(0.10)

            if(self.grid._game_over):
                pygame.draw.line(self._display_surf, RED, (0,0), (SCREEN_WIDTH-1, SCREEN_HEIGHT-1), 25)
                pygame.draw.line(self._display_surf, RED, (SCREEN_WIDTH-1,0), (0, SCREEN_HEIGHT-1), 25)
                pygame.display.flip()
                time.sleep(0.10)


        self.on_cleanup()
        
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()