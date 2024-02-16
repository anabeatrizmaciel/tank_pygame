import pygame
import random

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Tamanho do bônus
        self.image.fill((239, 84, 16))  # Cor do bônus (dourado)
        self.rect = self.image.get_rect()
        self.rect.x = 0  # A posição x será definida posteriormente
        self.rect.y = 0  # A posição y será definida posteriormente

    def generate_position(self, screen_width, screen_height, walls):
        # Gerar posição aleatória que não esteja sobre as paredes
        while True:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            if not pygame.sprite.spritecollide(self, walls, False):
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
