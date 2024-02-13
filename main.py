import random
from tank import Tank
from maze import Maze
from color import Color
import pygame
from list import labirinto_escolhido
import sys

def main():
    pygame.init()  #Inicialização do módulo pygame
    tela_largura = 800  #largura da tela
    tela_altura = 600  #altura da tela
    tela = pygame.display.set_mode((tela_largura, tela_altura))#janela do jogo com as dimensões especificadas
    color = Color()  #Instanciando a classe Color

    maze = Maze(tela_largura, tela_altura, color,
                labirinto_escolhido)  # Instancia a classe Maze com o labirinto aleatório escolhido
    maze.create_walls_group()#Cria um grupo de paredes com base na estrutura do labirinto


    # Criação de dois objetos do tipo Tank (os tanques do jogo)
    tanque1 = Tank((255,255,255), 150, tela_altura // 3, {'teclas': {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d}})
    tanque2 = Tank((0,0,0), tela_largura - 150, tela_altura // 3, {'teclas': {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT}})

    # Define o grupo de paredes para cada tanque para que eles possam verificar colisões
    tanque1.set_walls(maze.walls)
    tanque2.set_walls(maze.walls)

    todos_sprites = pygame.sprite.Group() #Criação de um grupo de sprites para todos os objetos do jogo
    todos_sprites.add(tanque1, tanque2)#Adiciona os tanques criados ao grupo de sprites

    # Inicialização de joysticks
    pygame.joystick.init()
    if pygame.joystick.get_count() >= 1:  # Se houver pelo menos um joystick conectado
        joystick1 = pygame.joystick.Joystick(0)#Cria um objeto joystick para o primeiro joystick conectado
        joystick1.init()#Inicializa o primeiro joystick
        tanque3_joystick1 = Tank(color.BLUE, 150, 2 * tela_altura // 3, {'joystick': joystick1})  # Cria um tanque associado ao primeiro joystick
        tanque3_joystick1.set_walls(maze.walls) #Configura as paredes para a detecção de colisão do tanque3
        todos_sprites.add(tanque3_joystick1)#Adiciona o tanque associado ao joystick ao grupo de sprites

    if pygame.joystick.get_count() >= 2:  # Se houver pelo menos dois joysticks conectados
        joystick2 = pygame.joystick.Joystick(1)
        joystick2.init()
        #Cria um tanque associado ao segundo joystick
        #A posição x é escolhida de modo a ser oposta à do primeiro tanque (neste caso, à direita da tela)
        #A posição y é a mesma do tanque associado ao primeiro joystick (tanque3)
        tanque4_joystick2 = Tank(color.YELLOW, tela_largura - 150, 2 * tela_altura // 3, {'joystick': joystick2})
        tanque4_joystick2.set_walls(maze.walls)#Configura as paredes para a detecção de colisão do tanque4
        todos_sprites.add(tanque4_joystick2)

    while True:  # Loop principal do jogo
        for evento in pygame.event.get():#Itera sobre todos os eventos do pygame
            if evento.type == pygame.QUIT:#Verifica se o evento é um pedido de sair do jogo
                pygame.quit() #Encerra os módulos do pygame corretamente.
                sys.exit()#Encerra o programa

        todos_sprites.update()#Atualiza todos os sprites do jogo

        tela.fill(color.BLACK)#Preenche a tela com a cor preta
        maze.draw(tela) #Desenha o labirinto na tela
        todos_sprites.draw(tela)#Desenha todos os sprites do grupo na tela
        pygame.display.flip()#Atualiza a tela inteira com tudo que foi desenhado desde a última atualização

        pygame.time.Clock().tick(60)#Limita ritmo de execução do jogo a 60 quadros por segundo

if __name__ == "__main__":
    main()#Chama a função principal do programa