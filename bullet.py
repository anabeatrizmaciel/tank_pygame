import pygame

class Bullet(pygame.sprite.Sprite):  # Define a classe Bullet que herda de pygame.sprite.Sprite
    def __init__(self, x, y, direction, color, screen_width, screen_height, walls, tanks=None, owner=None):
        # Método de inicialização da classe Bullet
        super().__init__()  # Chama o construtor da classe pai

        # Cria a imagem da bala
        self.image = pygame.Surface((5, 5))  # Cria uma superfície de 5x5 pixels
        self.image.fill(color)  # Preenche a superfície com a cor especificada
        self.rect = self.image.get_rect()  # Obtém um retângulo que delimita a bala
        self.rect.center = (x, y)  # Posiciona a bala no centro especificado pelas coordenadas (x, y)

        self.direction = direction  # Define a direção da bala
        self.speed = 5  # Define a velocidade da bala
        self.screen_width = screen_width  # Atribui a largura da tela à instância da bala
        self.screen_height = screen_height  # Atribui a altura da tela à instância da bala
        self.walls = walls  # Atribui as paredes passadas como parâmetro à instância da bala
        self.tanks = tanks if tanks is not None else []  # Atribui os tanques passados como parâmetro à instância da bala, ou uma lista vazia se não houver tanques
        self.owner = owner  # Atribui o dono da bala
        self.wall_collisions = 0  # Inicializa o contador de colisões com a parede

    def update(self):
        # Atualiza a posição da bala na tela
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Verifica se a bala saiu da tela e a destrói se isso ocorrer
        if not self.rect.colliderect(pygame.Rect(0, 0, self.screen_width, self.screen_height)):
            self.kill()

        # Verifica colisões com as paredes
        if self.walls:
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            if wall_hit_list:
                self.wall_collisions += 1
                if self.wall_collisions >= 3:
                    self.kill()  # Destrói a bala se ela colidir com a parede mais de 3 vezes
                else:
                    for wall in wall_hit_list:
                        # Inverte a direção da bala ao colidir com a parede
                        if self.direction == "up":
                            self.direction = "down"
                        elif self.direction == "down":
                            self.direction = "up"
                        elif self.direction == "left":
                            self.direction = "right"
                        elif self.direction == "right":
                            self.direction = "left"
                        self.speed *= 2  # Ajusta a velocidade
                        break

        # Verifica colisões com os tanques
        for tank in self.tanks:
            if tank is not None and self.owner is not None and tank != self.owner and tank.id is not None and self.owner.id is not None and tank.id != self.owner.id:  # Verifica se o tanque não é o dono da bala
                if pygame.sprite.collide_rect(self, tank):
                    tank.hit() #Registra que o tanque foi atingido
                    self.kill()  #Destrói a bala
                    break
