import pygame
from camera import camera

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, scale=None):
        key = (image, scale)
        if key in loaded:
            self.image = loaded[key]
        else:
            raw_image = pygame.image.load(image).convert_alpha()
            if scale:
                self.image = pygame.transform.scale(raw_image, scale)
            else:
                self.image = raw_image
            loaded[key] = self.image
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.entity.x - camera.x, self.entity.y - camera.y))

        