import pygame
import random
from operator import add, sub
import math
import app

# Screen and grid configuration
GRID_STEPS = 5  # Size of each grid cell in pixels
GRID_WIDTH = 100  # Number of cells horizontally
GRID_HEIGHT = 100  # Number of cells vertically
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH  # Total screen width in pixels
SCREEN_HEIGHT = GRID_STEPS * GRID_HEIGHT  # Total screen height in pixels

BACKGROUND_COLOR = (235, 235, 235)  # Background color of the window
FPS = 100  # Frames per second

# Cell types
INVALID_SPACE = -1  # Used for out-of-bounds checks
EMPTY_SPACE = 0     # Empty cell
GRAIN = 1           # Sand grain cell

GRAIN_COLOR = (130, 130, 75)  # Color of sand grains

class SandGameLogic:
    # The grid is a flat list representing the 2D grid
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)
    generating = False  # Whether the user is currently generating sand
    (genx, geny) = (0, 0)  # Mouse position for sand generation

    def __init__(self):
        self._game_over = False
        # Place a random grain at start
        random.seed
        (i, j) = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        self.set_item(i, j, GRAIN)

    def get_item(self, i, j):
        # Return the value at grid cell (i, j), or INVALID_SPACE if out of bounds
        if i >= 0 and i < GRID_WIDTH and j >= 0 and j < GRID_HEIGHT:
            return self.grid[j*GRID_WIDTH + i]
        return INVALID_SPACE

    def process_event(self, event: pygame.event.Event):
        # Handle mouse events for sand generation
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
        # If generating, add a grain at the mouse position
        if self.generating:
             self.set_item(math.floor(self.genx/GRID_STEPS), math.floor(self.geny/GRID_STEPS), GRAIN)
        # Update all grains from bottom to top
        for j in reversed(range(0, GRID_HEIGHT)):
            for i in range(0, GRID_WIDTH):
                # If this cell is a grain and not at the bottom
                if self.get_item(i, j) == GRAIN and j < GRID_HEIGHT-1:
                    # Try to move grain down if possible
                    if self.get_item(i, j+1) == EMPTY_SPACE:
                        self.set_item(i, j, EMPTY_SPACE)
                        self.set_item(i, j+1, GRAIN)
                    else:
                        # Try to move grain diagonally left or right
                        shift = random.randint(0, 1)*2 - 1
                        if self.get_item(i+shift, j+1) == EMPTY_SPACE:
                            self.set_item(i, j, EMPTY_SPACE)
                            self.set_item(i+shift, j+1, GRAIN)
                        elif self.get_item(i+(shift*-1), j+1) == EMPTY_SPACE:
                            self.set_item(i, j, EMPTY_SPACE)
                            self.set_item(i+(shift*-1), j+1, GRAIN)
                #elif self.get_item(i, j) == EMPTY_SPACE:
                    # No action needed for empty space, but keep grid updated
                #    self.set_item(i, j, EMPTY_SPACE)
        
    def render(self, surface):
        # Draw all grains on the surface
        for j in range(0, GRID_HEIGHT):
            for i in range(0, GRID_WIDTH):
                if self.get_item(i, j) == GRAIN:
                    pygame.draw.rect(surface, GRAIN_COLOR,
                                     pygame.Rect(i*GRID_STEPS,
                                             j*GRID_STEPS,
                                             GRID_STEPS,
                                             GRID_STEPS))

    def set_item(self, i, j, item):
        # Set the value of a grid cell (i, j)
        self.grid[j*GRID_WIDTH + i] = item
        
if __name__ == "__main__" :
    # Run the sand simulation using the App framework
    theApp = app.App(SandGameLogic(), SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS)
    theApp.on_execute()