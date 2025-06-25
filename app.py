import pygame
import time

RED = (255, 0, 0)

class App:
    def __init__(self, game, screen_width, screen_height, background_color, fps):
        self._running = True
        #self._display_surf = None
        self.size = self.weight, self.height = screen_width, screen_height
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = background_color
        self.mspf = (1/fps)*1000

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
                self.game.process_event(event)
                self._tick = False

    def on_loop(self):
        self.game.tick()

    def on_render(self):
        self._display_surf.fill(pygame.Color(self.background_color))
        self.game.render(self._display_surf)
        pygame.display.flip()
            
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            ticks = pygame.time.get_ticks()
            if((ticks - self._last_tick > self.mspf) and not self._pause and not self.game._game_over):
                self._tick = True
                self._last_tick = ticks
                self.on_loop()
                self.on_render()
            else:
                time.sleep(self.mspf/1000)

            if(self.game._game_over):
                pygame.draw.line(self._display_surf, RED, (0,0), (self.screen_width-1, self.screen_height-1), 25)
                pygame.draw.line(self._display_surf, RED, (self.screen_width-1,0), (0, self.screen_height-1), 25)
                pygame.display.flip()
                time.sleep(0.10)

        self.on_cleanup()