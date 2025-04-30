import pygame
from camera import camera

image_path = "CSP1123-TT3L-3-11/MAP/images"

loaded = {}

class Sprite:
    def __init__(self, image, is_ui=False, scale=None):
        from engine import engine
        self.is_ui = is_ui
        self.scale = scale
        self.image_name = image

        # Load image with optional scaling
        self.image = self.load_image(image, scale)
        engine.drawables.append(self)

    def load_image(self, image, scale=None):
        key = (image, scale)
        if key in loaded:
            return loaded[key]
        else:
            img = pygame.image.load(image_path + "/" + image).convert_alpha()
            if scale:
                img = pygame.transform.scale(img, scale)
            loaded[key] = img
            return img

    def set_image(self, image, scale=None):
        self.image_name = image
        self.scale = scale
        self.image = self.load_image(image, scale)

    def breakdown(self):
        from engine import engine
        engine.drawables.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else \
                (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)
        