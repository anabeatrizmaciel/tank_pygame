import pygame
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, brick_image):
        super().__init__()
        self.image = brick_image
        self.rect = self.image.get_rect(topleft=(x, y))