import pygame
from wall import Wall

class Maze:

    def __init__(self, largura, altura, colors, maze_structure):
        self.largura = largura
        self.altura = altura
        self.colors = colors
        self.maze_structure = maze_structure  #Representação da estrutura do labirinto
        self.wall_color = self.colors.random_color_wall()#Seleciona uma cor aleatória para as paredes
        self.background_color = self.colors.random_color_background(self.wall_color) #Seleciona uma cor aleatória para o fundo, diferente da cor das paredes
        self.walls = pygame.sprite.Group() #Cria um grupo de sprites para armazenar as paredes do labirinto
        self.create_walls_group()  #Chama o método para criar as paredes com base na estrutura do labirinto

    def create_walls_group(self):
        cell_height = 40
        brick_height = 50
        brick_image = pygame.image.load("assets/bricks1.png").convert_alpha()
        brick_image = pygame.transform.scale(brick_image, (brick_height, brick_height))

        for y, row in enumerate(self.maze_structure):
            for x, cell in enumerate(row):
                if cell == "#":
                    wall = Wall(x * cell_height, y * cell_height * 0.4, brick_image)
                    self.walls.add(wall)
    def draw(self, tela):
        tela.fill(self.background_color)  # Preenche o fundo com a cor aleatória selecionada

        for wall in self.walls: 
            tela.blit(wall.image, wall.rect) #Desenha cada parede na tela