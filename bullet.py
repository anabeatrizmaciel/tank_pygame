import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, screen_width, screen_height, walls, tanks=None, owner=None):
        super().__init__()

        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direction = direction
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = walls
        self.tanks = tanks if tanks is not None else []
        self.owner = owner
        self.wall_collisions = 0

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if not self.rect.colliderect(pygame.Rect(0, 0, self.screen_width, self.screen_height)):
            self.kill()

        if self.walls:
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            if wall_hit_list:
                self.wall_collisions += 1
                if self.wall_collisions >= 3:
                    self.kill()
                else:
                    for wall in wall_hit_list:
                        if self.direction == "up":
                            self.rect.x -= 18
                            self.direction = "down"
                        elif self.direction == "down":
                            self.direction = "up"
                            self.rect.x -= 18
                        elif self.direction == "left":
                            self.direction = "right"
                            self.rect.y -= 15
                        elif self.direction == "right":
                            self.direction = "left"
                            self.rect.y -= 15
                        break

        for tank in self.tanks:
            if tank is not None and self.owner is not None and tank != self.owner and tank.id is not None and self.owner.id is not None and tank.id != self.owner.id:
                if pygame.sprite.collide_rect(self, tank):
                    tank.hit()
                    self.kill()
                    break
