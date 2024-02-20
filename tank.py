import pygame
from bullet import Bullet

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, id, controls, bullets, screen_width, screen_height, walls=None,
                 spritesheet_path=None):
        super().__init__()

        self.spritesheet_path = spritesheet_path
        self.current_frame = 0
        self.animation_frames = 4
        if id == 1:  # Only for tank 1
            self.current_frame = 1
        else:
            self.current_frame = 0
        self.quick_rotate_angle = 0
        self.quick_rotate_timer = 0
        self.quick_rotate_duration = 500
        self.spritesheet_path = spritesheet_path
        self.load_spritesheet()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = 5
        self.id = id
        self.control_keys = controls.get('teclas')
        self.joystick = None
        self.bullets = bullets
        self.walls = walls
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = 3
        self.hit_counter = 0
        self.direction = "up"
        self.can_shoot = True

    def load_spritesheet(self):
        spritesheet = pygame.image.load(self.spritesheet_path)
        self.sprite_width = spritesheet.get_width() // 4
        self.sprite_height = spritesheet.get_height()
        self.frames = [spritesheet.subsurface((i * self.sprite_width, 0, self.sprite_width, self.sprite_height)) for i in range(4)]
        self.image = self.frames[self.current_frame]

    def animate(self):
        self.current_frame = (self.current_frame + 1) % 4
        self.image = self.frames[self.current_frame]

    def increment_lives(self):
        self.lives += 1

    def set_walls(self, walls):
        self.walls = walls

    def track_controls(self, keys):
        if keys[self.control_keys['cima']]:
            self.rect.y -= self.velocity
            self.direction = "up"
            self.current_frame = 0
            self.animate()
        if keys[self.control_keys['baixo']]:
            self.rect.y += self.velocity
            self.direction = "down"
            self.current_frame = 1
            self.animate()
        if keys[self.control_keys['esquerda']]:
            self.rect.x -= self.velocity
            self.direction = "left"
            self.current_frame = 2
            self.animate()
        if keys[self.control_keys['direita']]:
            self.rect.x += self.velocity
            self.direction = "right"
            self.current_frame = 3
            self.animate()
        if keys[self.control_keys['esquerda']] or keys[self.control_keys['direita']] or keys[self.control_keys['cima']] or keys[self.control_keys['baixo']]:
            self.animate()

    def fire_bullet(self, direction, enemy_tanks):
        self.can_shoot = not any(bullet.alive() for bullet in self.bullets)

        if self.alive() and self.can_shoot:
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

    def rotate_quickly(self):
        rotated_sprite = pygame.transform.rotate(self.image, self.quick_rotate_angle)
        self.image = rotated_sprite

    def hit(self):
        if self.lives > 0:
            self.lives -= 1
            self.quick_rotate_angle = 90  # Ângulo para a rotação rápida
            self.quick_rotate_timer = pygame.time.get_ticks()  # Configura o temporizador
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
            self.rect.x += int(x_axis * self.velocity)
            self.rect.y += int(y_axis * self.velocity)

            if joystick.get_button(0):
                self.fire_bullet(self.direction)

        elif self.control_keys:
            keys = pygame.key.get_pressed()
            self.track_controls(keys)

            if self.walls and pygame.sprite.spritecollideany(self, self.walls):
                self.rect.x = old_x
                self.rect.y = old_y

        for bullet in self.bullets:
            bullet.update()

        if self.quick_rotate_timer > 0:
            elapsed_time = pygame.time.get_ticks() - self.quick_rotate_timer
            if elapsed_time >= self.quick_rotate_duration:
                self.quick_rotate_timer = 0
                self.quick_rotate_angle = 0
            else:
                self.rotate_quickly()
