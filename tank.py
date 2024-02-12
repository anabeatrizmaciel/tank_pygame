import pygame

# Define os tanques
class Tank(pygame.sprite.Sprite):#classe Tank herda de pygame.sprite.Sprite
    def __init__(self, cor, pos_x, pos_y, controles):#Inicialização da classe
        super().__init__()#Inicializa a classe pai pygame.sprite.Sprite

        self.image = pygame.Surface((50, 30))#Cria uma superfície para representar a imagem do tanque - Surface (Largura, Altura)
        self.image.fill(cor)#Preenche a superfície com a cor especificada
        self.rect = self.image.get_rect(center=(pos_x, pos_y))#Obtém um retângulo que representa a posição do tanque na tela
        self.teclas_controle = controles.get('teclas', None)#Dicionário das teclas de controle
        self.joystick = controles.get('joystick', None)#Joystick associado (pode nao ter nenhum None)
        self.velocidade = 5#Velocidade de movimento do tanque

    def update(self):#Método para atualizar a posição do tanque
        if self.joystick:# Se houver um joystick associado, atualiza com base nele
            joystick_inputs = [self.joystick.get_axis(0), self.joystick.get_axis(1)]#Pega os valores dos eixos do joystick
            self.rect.x += int(joystick_inputs[0] * self.velocidade)#Atualiza a posição do tanque com base nos controles do joystick
            self.rect.y += int(joystick_inputs[1] * self.velocidade)
        elif self.teclas_controle:#Senão, atualiza com base nas teclas
            teclas = pygame.key.get_pressed()#Pega o estado das teclas pressionadas
            if teclas[self.teclas_controle['esquerda']]:#Se a tecla esquerda estiver pressionada
                self.rect.x -= self.velocidade#Move o tanque para a esquerda
            if teclas[self.teclas_controle['direita']]:#Se a tecla direita estiver pressionada
                self.rect.x += self.velocidade#Move o tanque para a direita
            if teclas[self.teclas_controle['cima']]:#Se a tecla cima estiver pressionada
                self.rect.y -= self.velocidade#Move o tanque para cima
            if teclas[self.teclas_controle['baixo']]:#Se a tecla baixo estiver pressionada
                self.rect.y += self.velocidade#Move o tanque para baixo
