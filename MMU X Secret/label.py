import pygame
import os
import sys

fonts = {}

anti_alias = True
font_folder_path = "fonts"

def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和打包后"""
    if hasattr(sys, '_MEIPASS'):  # 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Label:
    def __init__(self, font, text, size=32, color=(255, 255, 255)):
        from engine import engine
        global labels
        self.color = color
        name = font+str(size)
        if name in fonts:
            self.font = fonts[name]
        else:
            self.font = pygame.font.Font(resource_path(os.path.join(font_folder_path, font)), size)
            fonts[name] = self.font

        self.set_text(text)
        engine.ui_drawables.append(self)

    def breakdown(self):
        from engine import engine
        engine.ui_drawables.remove(self)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, anti_alias, self.color)
        self.shadow_surface = self.font.render(self.text, anti_alias, (0,0,0))

    def get_bounds(self):
        return pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

    def draw(self, screen):
        screen.blit(self.shadow_surface, (self.entity.x+1, self.entity.y+1))
        screen.blit(self.surface, (self.entity.x, self.entity.y))