import pygame
from bullet import Bullet
from color import Color

class Tank(pygame.sprite.Sprite):
    def __init__(self, color, x, y, id, controls, bullets, screen_width, screen_height, walls=None):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = 5
        self.id = id
        self.teclas_controle = controls.get('teclas')
        self.joystick = None
        self.bullets = bullets
        self.walls = walls  #armazenar as paredes do labirinto
        self.screen_width = screen_width
        self.screen_height = screen_height
        #self.enemy_tanks = enemy_tanks  #tanques adversários

    def set_walls(self, walls):
        self.walls = walls

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

    def fire_bullet(self, direction):
        print(f"Tanque {self.id} disparando bala na direção {direction}!")
        bullet_color = (255, 0, 0) if self.id == 1 else (0, 255, 0)  # Exemplo de cor diferente por tanque
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction, bullet_color, self.screen_width,
                        self.screen_height, self.walls)  # Passa as paredes para a bala
        self.bullets.add(bullet)  #Adiciona a bala ao grupo de balas

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y

        if self.joystick:
            joystick = self.joystick
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)
            self.rect.x += int(x_axis * self.velocidade)
            self.rect.y += int(y_axis * self.velocidade)

            if joystick.get_button(0):  # Verifica se o botão do joystick foi pressionado
                self.fire_bullet(self.direction)  # Passando a direção atual para a bala

        elif self.teclas_controle:
            keys = pygame.key.get_pressed()
            self.track_controls(keys)

            if self.walls and pygame.sprite.spritecollideany(self, self.walls):
                self.rect.x = old_x
                self.rect.y = old_y

        for bullet in self.bullets:  # Itera sobre cada bala
            bullet.update()  # Atualiza a bala
