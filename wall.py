import pygame
from color import Color

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, wall_color):
        super().__init__() #Herda da classe pygame.sprite.Sprite para que possa ser tratada como um sprite
        #self.colors = colors #Instância da classe Color
        self.image = pygame.Surface((largura, altura))#Cria a imagem (surpeficie) da parede
        self.image.fill(wall_color)  # Preenche a superfície com a cor escolhida para a parede
 #Escolhe uma cor aleatória da instância de Color
        self.rect = self.image.get_rect(topleft = (x, y)) #Obtém um retângulo que representa a posição e o tamanho da parede na tela
