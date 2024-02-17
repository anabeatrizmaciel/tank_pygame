import pygame
from bullet import Bullet

class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y, id, controls, bullets, screen_width, screen_height, walls=None,
                 image_path_tanque_1=None, image_path_tanque_2=None):
        super().__init__()

        self.image_path_tanque_1 = image_path_tanque_1
        self.image_path_tanque_2 = image_path_tanque_2
        self.current_image_path = self.image_path_tanque_1
        self.load_image()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocidade = 5
        self.id = id
        self.teclas_controle = controls.get('teclas')
        self.joystick = None
        self.bullets = bullets
        self.walls = walls
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = 3
        self.hit_counter = 0
        self.direction = "up"

    def increment_lives(self):
        self.lives += 1

    def set_walls(self, walls):
        self.walls = walls

    def load_image(self):
        self.image = pygame.image.load(self.current_image_path)

    def track_controls(self, keys):
        if keys[self.teclas_controle['cima']]:
            self.rect.y -= self.velocidade
            self.direction = "up"
        if keys[self.teclas_controle['baixo']]:
            self.rect.y += self.velocidade
            self.direction = "down"
        if keys[self.teclas_controle['esquerda']]:
            self.rect.x -= self.velocidade
            self.direction = "left"
        if keys[self.teclas_controle['direita']]:
            self.rect.x += self.velocidade
            self.direction = "right"

    def fire_bullet(self, direction, enemy_tanks):
        if self.alive():
            bullet_color = (255, 0, 0) if self.id == 1 else (0, 255, 0)
            enemy_tanks = [tank for tank in enemy_tanks if tank is not None and tank.id != self.id]
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, bullet_color, self.screen_width,
                            self.screen_height, self.walls, enemy_tanks, owner=self)
            self.bullets.add(bullet)

    def hit(self):
        if self.lives > 0:
            self.lives -= 1
            print(f"Tank ID {self.id} hit! Lives remaining: {self.lives}")
            if self.lives == 0:
                self.kill()
                self.image.set_alpha(0)

    def update(self):
        if not self.alive():
            return

        old_x = self.rect.x
        old_y = self.rect.y

        if self.joystick:
            joystick = self.joystick
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)
            self.rect.x += int(x_axis * self.velocidade)
            self.rect.y += int(y_axis * self.velocidade)

            if joystick.get_button(0):
                self.fire_bullet(self.direction)

        elif self.teclas_controle:
            keys = pygame.key.get_pressed()
            self.track_controls(keys)

            if self.walls and pygame.sprite.spritecollideany(self, self.walls):
                self.rect.x = old_x
                self.rect.y = old_y

        for bullet in self.bullets:
            bullet.update()
