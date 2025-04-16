from unittest import loader
import pygame

sprites = []
load = {}

class Sprite:
    def __init__(self, image, x, y):
        if image in loader:
            self.image = loader[image]
        else:
            self.image = pygame.image.load(image)
            loader[image] = self.image
        self.x = x
        self.y = y
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))