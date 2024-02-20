import pygame
import random

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Bonus' size
        self.image.fill((239, 84, 16))  # Bonus' color (golden)
        self.rect = self.image.get_rect()
        self.rect.x = 0  # X position will be defined afterward
        self.rect.y = 0  # Y position will be defined afterward

    def generate_position(self, screen_width, screen_height, walls):
        # Generate random position that isn't in the walls
        while True:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            if not pygame.sprite.spritecollide(self, walls, False):
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
