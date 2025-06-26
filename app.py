import pygame
import time

RED = (255, 0, 0)

class App:
    def __init__(self, game, screen_width, screen_height, background_color, fps):
        self._running = True
        #self._display_surf = None
        self.size = self.weight, self.height = screen_width, screen_height  # Set window size
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = background_color
        self.mspf = (1/fps)*1000  # Milliseconds per frame

    def on_init(self):
        pygame.init()  # Initialize pygame
        self._display_surf = pygame.display.set_mode(self.size, pygame.SHOWN)  # Create window
        self._running = True
        self._step = False
        self._tick = False
        self._pause = False
        self._last_tick = 0  # Track last tick time

    def on_event(self, event):
        # Handle window close event
        if event.type == pygame.QUIT:
            self._running = False
        # Handle key events
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_SPACE):
                self._pause = not self._pause  # Toggle pause on spacebar
            if(self._tick == True):
                self.game.process_event(event)  # Pass event to game logic
                self._tick = False
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
            self.game.process_event(event)
            
    def on_loop(self):
        self.game.tick()  # Advance game logic

    def on_render(self):
        self._display_surf.fill(pygame.Color(self.background_color))  # Clear screen
        self.game.render(self._display_surf)  # Draw game
        pygame.display.flip()  # Update display
            
    def on_cleanup(self):
        pygame.quit()  # Quit pygame

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            # Process all pygame events
            for event in pygame.event.get():
                self.on_event(event)

            ticks = pygame.time.get_ticks()
            # Only update game if enough time has passed, not paused, and not game over
            if((ticks - self._last_tick > self.mspf) and not self._pause and not self.game._game_over):
                self._tick = True
                self._last_tick = ticks
                self.on_loop()
                self.on_render()
            else:
                time.sleep(self.mspf/1000)  # Sleep to limit frame rate

            # If game over, draw red X and update display
            if(self.game._game_over):
                pygame.draw.line(self._display_surf, RED, (0,0), (self.screen_width-1, self.screen_height-1), 25)
                pygame.draw.line(self._display_surf, RED, (self.screen_width-1,0), (0, self.screen_height-1), 25)
                pygame.display.flip()
                time.sleep(0.10)

        self.on_cleanup()  # Clean up