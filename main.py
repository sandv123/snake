import pygame
import random
from operator import add, sub
import app

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACKGROUND_COLOR = (70, 130, 130)
SNAKE_COLOR = (0, 255, 255)

FPS = 8
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
GRID_HIGHT = 20
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH
SCREEN_HIGHT = GRID_STEPS * GRID_HIGHT

class GameLogic:
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HIGHT)

    snakeDir: tuple = LEFT
    snakePos = (0, 0)
    snakeTail = list()

    applePos = (0, 0)
    
    def __init__(self) -> None:
        self._game_over = False
        random.seed
        self.snakePos = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HIGHT-1))
        (taili, tailj) = tuple(map(sub, self.snakePos, self.snakeDir))
        self.snakeTail.append((taili,tailj))

        (i, j) = self.snakePos
        self.set_item(i, j, SNAKE_HEAD)
        self.set_item(i, j, SNAKE_TAIL)

        self.new_apple()

    def new_apple(self):
        self.applePos = (applei, applej) = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HIGHT-1))
        self.set_item(applei, applej, APPLE)

    def get_item(self, i, j):
        return self.grid[j*GRID_WIDTH + i]
    
    def set_item(self, i, j, item):
        self.grid[j*GRID_WIDTH + i] = item
    
    def clear_grid(self):
        self.grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HIGHT)

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
        if(nextj > GRID_HIGHT-1):
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

    def draw_shape(self, surface, i, j):
        if(self.get_item(i,j) == SNAKE_HEAD):
            center = (i*GRID_STEPS + GRID_STEPS/2, j*GRID_STEPS + GRID_STEPS/2)
            pygame.draw.circle(surface,
                            SNAKE_COLOR,
                            center,
                            GRID_STEPS/2,)
            
        elif(self.get_item(i, j) == SNAKE_TAIL):
            pygame.draw.rect(surface, pygame.Color(255,255,255),
                                    pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS),
                                    0)
        elif(self.get_item(i,j) == APPLE):
            center = (i*GRID_STEPS + GRID_STEPS/2, j*GRID_STEPS + GRID_STEPS/2)
            pygame.draw.circle(surface,
                            RED,
                            center,
                            GRID_STEPS/2,)
        elif(self.get_item(i, j) == EMPTY_SPACE):
            pygame.draw.rect(surface, pygame.Color(0,200,150),
                                    pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS),
                                             1)
    def render(self, surface):
        for j in range(0, GRID_HIGHT):
            for i in range(0, GRID_WIDTH):
                self.draw_shape(surface, i, j)

    def process_event(self, event):
        if(event.key == pygame.K_UP and self.snakeDir != DOWN):
            self.snakeDir = UP
        if(event.key == pygame.K_DOWN and self.snakeDir != UP):
            self.snakeDir = DOWN
        if(event.key == pygame.K_LEFT and self.snakeDir != RIGHT):
            self.snakeDir = LEFT
        if(event.key == pygame.K_RIGHT and self.snakeDir != LEFT):
            self.snakeDir = RIGHT
        
if __name__ == "__main__" :
    theApp = app.App(GameLogic(), SCREEN_WIDTH, SCREEN_HIGHT, BACKGROUND_COLOR, FPS)
    theApp.on_execute()