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

# Grid item types
EMPTY_SPACE = 0
SNAKE_HEAD = 1
SNAKE_TAIL = 2
APPLE = 3

# Directions (as (dx, dy) tuples)
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Screen and grid dimensions
GRID_STEPS = 29
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH
SCREEN_HEIGHT = GRID_STEPS * GRID_HEIGHT

class SnakeGameLogic:
    # The game grid, a flat list representing the 2D grid
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)

    # Snake direction, position, and tail
    snakeDir: tuple = LEFT
    snakePos = (0, 0)
    snakeTail = list()

    # Apple position
    applePos = (0, 0)
    
    def __init__(self) -> None:
        self._game_over = False
        random.seed()
        # Initialize snake head at random position
        self.snakePos = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        # Place initial tail segment behind the head
        (taili, tailj) = tuple(map(sub, self.snakePos, self.snakeDir))
        self.snakeTail.append((taili,tailj))

        (i, j) = self.snakePos
        self.set_item(i, j, SNAKE_HEAD)
        self.set_item(i, j, SNAKE_TAIL)

        self.new_apple()

    def new_apple(self):
        # Place a new apple at a random position
        self.applePos = (applei, applej) = (random.randint(1, GRID_WIDTH-1), random.randint(1, GRID_HEIGHT-1))
        self.set_item(applei, applej, APPLE)

    def get_item(self, i, j):
        # Get the item at grid position (i, j)
        return self.grid[j*GRID_WIDTH + i]
    
    def set_item(self, i, j, item):
        # Set the item at grid position (i, j)
        self.grid[j*GRID_WIDTH + i] = item
    
    def clear_grid(self):
        # Reset the grid to all empty spaces
        self.grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)

    def update_grid(self):
        # Update the grid with the snake and apple positions
        (i, j) = self.snakePos
        self.set_item(i, j, SNAKE_HEAD)

        for (i, j) in self.snakeTail:
            self.set_item(i, j, SNAKE_TAIL)

        (i, j) = self.applePos
        self.set_item(i, j, APPLE)

    def tick(self):
        # Advance the game state by one tick (move the snake, check collisions, etc.)
        (nexti, nextj) = tuple(map(add, self.snakePos, self.snakeDir))

        # Wrap around screen edges
        if(nexti < 0):
            nexti = GRID_WIDTH-1
        if(nextj < 0):
            nextj = GRID_WIDTH-1
        if(nexti > GRID_WIDTH-1):
            nexti = 0
        if(nextj > GRID_HEIGHT-1):
            nextj = 0

        # Move snake based on what is in the next cell
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
        # Draw the appropriate shape for the grid cell at (i, j)
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
        # Render the entire grid to the surface
        for j in range(0, GRID_HEIGHT):
            for i in range(0, GRID_WIDTH):
                self.draw_shape(surface, i, j)

    def process_event(self, event: pygame.event.Event):
        # Handle keyboard events to change snake direction
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_UP and self.snakeDir != DOWN):
                self.snakeDir = UP
            if(event.key == pygame.K_DOWN and self.snakeDir != UP):
                self.snakeDir = DOWN
            if(event.key == pygame.K_LEFT and self.snakeDir != RIGHT):
                self.snakeDir = LEFT
            if(event.key == pygame.K_RIGHT and self.snakeDir != LEFT):
                self.snakeDir = RIGHT
        
if __name__ == "__main__" :
    # Run the game if this file is executed directly
    theApp = app.App(SnakeGameLogic(), SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS)
    theApp.on_execute()