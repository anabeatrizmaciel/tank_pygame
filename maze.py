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
        tamanho_celula = 40
        wall_color = self.colors.random_color_wall()#Escolhe uma cor aleatória para todas as paredes
        for y, row in enumerate(self.maze_structure): #y retorna o numero do indice linha. ROW é o conteudo da linha
            for x, cell in enumerate(row):#x retorna o numero do indice coluna. CELL é o conteúdo da coluna x na linha ROW
                if cell == "#": #verifica se é uma parede.
                    #pygame.draw.rect(tela,  self.wall_color, (x * tamanho_celula, y * tamanho_celula, tamanho_celula, tamanho_celula))#Desenha um retângulo na tela representando a parede. Conforme a estrutura do labirinto.
                    wall = Wall(x * tamanho_celula, y * tamanho_celula, tamanho_celula, tamanho_celula,
                                wall_color) #Cria um sprite de parede na posicao passada
                    self.walls.add(wall)#Adiciona o sprite de parede ao grupo de paredes

    def draw(self, tela):
        tela.fill(self.background_color)  # Preenche o fundo com a cor aleatória selecionada
        # cor_parede = self.colors.cor_aleatoria()  # Seleciona uma cor aleatória para as paredes

        for parede in self.walls:  #Desenha os sprites das paredes
            tela.blit(parede.image, parede.rect) #Desenha cada parede na tela