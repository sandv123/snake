import pygame
import random
from operator import add, sub
import math
import app

# Screen dimensions
GRID_STEPS = 5
GRID_WIDTH = 100
GRID_HEIGHT = 100
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH
SCREEN_HEIGHT = GRID_STEPS * GRID_HEIGHT

BACKGROUND_COLOR = (235, 235, 235)
FPS = 100

INVALID_SPACE = -1
EMPTY_SPACE = 0
GRAIN = 1

GRAIN_COLOR = (130, 130, 75)

class SandGameLogic:
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)
    generating = False
    (genx, geny) = (0, 0)

    def __init__(self):
        self._game_over = False
        #self.x = 0
        random.seed
        (i, j) = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        self.set_item(i, j, GRAIN)

    def get_item(self, i, j):
        if i >= 0 and i < GRID_WIDTH and j >= 0 and j < GRID_HEIGHT:
            return self.grid[j*GRID_WIDTH + i]
        return INVALID_SPACE

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                self.generating = True
                (self.genx, self.geny) = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.generating = False
        if event.type == pygame.MOUSEMOTION:
             (self.genx, self.geny) = event.pos

    def tick(self):
        if self.generating:
             self.set_item(math.floor(self.genx/GRID_STEPS), math.floor(self.geny/GRID_STEPS), GRAIN)
        for j in reversed(range(0, GRID_HEIGHT)):
            for i in range(0, GRID_WIDTH):
                if self.get_item(i, j) == GRAIN and j < GRID_HEIGHT-1:  # Need to drop the grain
                    if self.get_item(i, j+1) == EMPTY_SPACE:                # Can drop down?
                        self.set_item(i, j, EMPTY_SPACE)
                        self.set_item(i, j+1, GRAIN)
                    else:
                        shift = random.randint(0, 1)*2 - 1                  
                        if self.get_item(i+shift, j+1) == EMPTY_SPACE:              # Can drop randomly left or right?
                            self.set_item(i, j, EMPTY_SPACE)
                            self.set_item(i+shift, j+1, GRAIN)
                        elif self.get_item(i+(shift*-1), j+1) == EMPTY_SPACE:       # Can drop the other way?
                            self.set_item(i, j, EMPTY_SPACE)
                            self.set_item(i+(shift*-1), j+1, GRAIN)
                elif self.get_item(i, j) == EMPTY_SPACE:                # Do nothing with empty space
                    self.set_item(i, j, EMPTY_SPACE)
        
    def render(self, surface):
        for j in range(0, GRID_HEIGHT):
            for i in range(0, GRID_WIDTH):
                if self.get_item(i, j) == GRAIN:
                    pygame.draw.rect(surface, GRAIN_COLOR,
                                     pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS))

    def set_item(self, i, j, item):
        #self.grid_new[j*GRID_WIDTH + i] = item
        self.grid[j*GRID_WIDTH + i] = item
        
if __name__ == "__main__" :
    theApp = app.App(SandGameLogic(), SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS)
    theApp.on_execute()