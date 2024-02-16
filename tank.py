import pygame
from bullet import Bullet

class Tank(pygame.sprite.Sprite):  # Define a classe Tank que herda de pygame.sprite.Sprite
    def __init__(self, color, x, y, id, controls, bullets, screen_width, screen_height, walls=None):
        # Método de inicialização da classe Tank
        super().__init__()  # Chama o construtor da classe pai

        # Cria a imagem do tanque
        self.image = pygame.Surface((30, 30)) #Cria uma superfície de 30x30 pixels
        self.image.fill(color) #Preenche a superfície com a cor especificada
        self.rect = self.image.get_rect()#Obtém um retângulo que delimita o tanque
        self.rect.center = (x, y) #posiciona o tanque no centro especificado pelas coordenadas (x, y)

        self.velocidade = 5  # Define a velocidade do tanque
        self.id = id  # Define o ID único do tanque
        self.teclas_controle = controls.get('teclas')  # Obtém as teclas de controle para o tanque
        self.joystick = None  # Inicializa a variável do joystick como None
        self.bullets = bullets  # Atribui as balas passadas como parâmetro à instância do tanque
        self.walls = walls  # Atribui as paredes passadas como parâmetro à instância do tanque
        self.screen_width = screen_width  # Atribui a largura da tela à instância do tanque
        self.screen_height = screen_height  # Atribui a altura da tela à instância do tanque
        self.lives = 3  # Inicializa o número de vidas do tanque
        self.hit_counter = 0  # Inicializa o contador de vezes que o tanque foi atingido

    def increment_lives(self):
        self.lives += 1
    def set_walls(self, walls):
        # Define as paredes do tanque
        self.walls = walls

    def track_controls(self, keys):
        # Controla o movimento do tanque com base nas teclas pressionadas
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
        # Dispara uma bala na direção especificada
        if self.alive():
            # Define a cor da bala com base no ID do tanque
            bullet_color = (255, 0, 0) if self.id == 1 else (0, 255, 0)
            # Filtra os tanques inimigos que não são nulos e ID é diferente do ID deste tanque
            enemy_tanks = [tank for tank in enemy_tanks if tank is not None and tank.id != self.id]
            # Cria uma bala e a adiciona ao grupo de balas
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, bullet_color, self.screen_width,
                            self.screen_height, self.walls, enemy_tanks, owner=self)
            self.bullets.add(bullet)

    def hit(self):
        # Registra que o tanque foi atingido e atualiza o número de vidas
        if self.lives > 0:
            self.lives -= 1
            print(f"Tank ID {self.id} hit! Lives remaining: {self.lives}")
            if self.lives == 0:
                self.kill()
                self.image.set_alpha(0)#FICA INVISIVEL

    def update(self):
        # Atualiza a posição do tanque na tela
        if not self.alive():
            return

        old_x = self.rect.x
        old_y = self.rect.y

        if self.joystick:
            # Controla o movimento do tanque com base no joystick
            joystick = self.joystick
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)
            self.rect.x += int(x_axis * self.velocidade)
            self.rect.y += int(y_axis * self.velocidade)

            if joystick.get_button(0):
                self.fire_bullet(self.direction)

        elif self.teclas_controle:
            # Controla o movimento do tanque com base nas teclas de controle
            keys = pygame.key.get_pressed()
            self.track_controls(keys)

            # Verifica colisões com as paredes
            if self.walls and pygame.sprite.spritecollideany(self, self.walls):
                self.rect.x = old_x
                self.rect.y = old_y
        for bullet in self.bullets:
            bullet.update()  #Atualiza as balas