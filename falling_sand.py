import pygame
import random
from operator import add, sub
import app

# Screen dimensions
GRID_STEPS = 10
GRID_WIDTH = 40
GRID_HEIGHT = 40
SCREEN_WIDTH = GRID_STEPS * GRID_WIDTH
SCREEN_HEIGHT = GRID_STEPS * GRID_HEIGHT

BACKGROUND_COLOR = (130, 130, 130)
FPS = 10

EMPTY_SPACE = 0

class SandGameLogic:
    grid = [EMPTY_SPACE] * (GRID_WIDTH * GRID_HEIGHT)

    def __init__(self):
        self._game_over = False

    def process_event(self, event):
        None
    def tick(self):
        None
    def render(self, surface):
        None

if __name__ == "__main__" :
    theApp = app.App(SandGameLogic(), SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS)
    theApp.on_execute()