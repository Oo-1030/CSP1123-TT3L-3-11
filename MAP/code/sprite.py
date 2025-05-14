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
        self._load_image(image)
        engine.drawables.append(self)

    def _load_image(self, image):
        global loaded
        full_path = image_path + "/" + image
        if (image, self.scale) in loaded:
            self.image = loaded[(image, self.scale)]
        else:
            img = pygame.image.load(full_path).convert_alpha()
            if self.scale:
                img = pygame.transform.scale(img, self.scale)
            self.image = img
            loaded[(image, self.scale)] = img

    def set_image(self, image, scale=None):
        self.image_name = image
        if scale is not None:
            self.scale = scale
        self._load_image(image)

    def breakdown(self):
        from engine import engine
        engine.drawables.remove(self)

    def draw(self, screen):
        pos = (self.entity.x - camera.x, self.entity.y - camera.y) \
                if not self.is_ui else \
                (self.entity.x, self.entity.y)
        screen.blit(self.image, pos)