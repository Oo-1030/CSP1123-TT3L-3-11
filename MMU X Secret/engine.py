import pygame
import os
import sys

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后"""
    if hasattr(sys, '_MEIPASS'):  # 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

music = pygame.mixer.music.load(resource_path("assets/gameMusic.mp3"))
pygame.mixer.music.play(-1)

engine = None
default_width = 1280
default_height = 720


class Engine:
    def __init__(self, game_title) -> None:
        from camera import create_screen
        global engine
        engine = self

        self.active_objs = [] # Anything with an update() method which can be called

        # Layers of what order things are drawn. UI Drawables draw over Background for example
        self.background_drawables = []
        self.drawables = [] # Anything to be drawn in the world
        self.ui_drawables = [] # Anything to be drawn over the world

        self.usables = []

        self.persistent_removed = dict()

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        self.stages = {}
        self.current_stage = None

    def register(self, stage_name, func):
        self.stages[stage_name] = func

    def switch_to(self, stage_name):
        from area import area
        area = None
        self.reset()
        self.current_stage = stage_name 
        func = self.stages[stage_name]
        print(f"Switching to {self.current_stage}")
        func()

    def run(self):
        from input import keys_down, mouse_buttons_down, \
                mouse_buttons_just_pressed, keys_just_pressed
        self.running = True
        while self.running:
            mouse_buttons_just_pressed.clear()
            keys_just_pressed.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    keys_down.add(event.key)
                    keys_just_pressed.add(event.key)
                elif event.type == pygame.KEYUP:
                    keys_down.discard(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_buttons_down.add(event.button)
                    mouse_buttons_just_pressed.add(event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_buttons_down.discard(event.button)

            # Update Code
            for a in self.active_objs:
                a.update()

            # Draw Code
            self.screen.fill(self.clear_color)
            
            # Draw background items like the tiles
            for b in self.background_drawables:
                b.draw(self.screen)


            # Draw the main objects
            for s in self.drawables:
                s.draw(self.screen)

            # Draw UI Stuff
            for l in self.ui_drawables:
                l.draw(self.screen)


            pygame.display.flip()

            # Cap the frames
            pygame.time.delay(17)
                
        pygame.quit()


    def reset(self):
        from physics import reset_physics
        reset_physics()
        self.active_objs.clear()
        self.drawables.clear()
        self.ui_drawables.clear()
        self.background_drawables.clear()
        self.usables.clear()