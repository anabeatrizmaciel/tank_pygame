import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, screen_width, screen_height, walls):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = walls  #paredes do labirinto como um atributo

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Verifica se a bala saiu da tela
        if not self.rect.colliderect(pygame.Rect(0, 0, self.screen_width, self.screen_height)):
            self.kill()

        # Verifica se a bala colide com alguma parede do labirinto
        if self.walls:
            for wall in self.walls:
                if self.rect.colliderect(wall.rect):
                    self.kill() #elimina a bullet
                    break
