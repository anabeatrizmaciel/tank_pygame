from game import Game
from tank import Tank
import pygame
import sys

def main():
    pygame.init()  #Inicialização do módulo pygame
    game_instance = Game()  #instância da classe Game

    tela_largura = 800  #largura da tela
    tela_altura = 600  #altura da tela
    tela = pygame.display.set_mode((tela_largura, tela_altura))#janela do jogo com as dimensões especificadas
    PRETO = (0, 0, 0)
    VERDE = (0, 255, 0)
    VERMELHO = (255, 0, 0)
    AZUL = (0, 0, 255)
    AMARELO = (255, 255, 0)

    # Criação de dois objetos do tipo Tank (os tanques do jogo)
    tanque1 = Tank(VERDE, 150, tela_altura // 3, {'teclas': {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d}})
    tanque2 = Tank(VERMELHO, tela_largura - 150, tela_altura // 3, {'teclas': {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT}})

    todos_sprites = pygame.sprite.Group() #Criação de um grupo de sprites para todos os objetos do jogo
    todos_sprites.add(tanque1, tanque2)#Adiciona os tanques criados ao grupo de sprites

    # Inicialização de joysticks
    pygame.joystick.init()
    if pygame.joystick.get_count() >= 1:  # Se houver pelo menos um joystick conectado
        joystick1 = pygame.joystick.Joystick(0)#Cria um objeto joystick para o primeiro joystick conectado
        joystick1.init()#Inicializa o primeiro joystick
        tanque3_joystick1 = Tank(AZUL, 150, 2 * tela_altura // 3, {'joystick': joystick1})  # Cria um tanque associado ao primeiro joystick
        todos_sprites.add(tanque3_joystick1)#Adiciona o tanque associado ao joystick ao grupo de sprites

    if pygame.joystick.get_count() >= 2:  # Se houver pelo menos dois joysticks conectados
        joystick2 = pygame.joystick.Joystick(1)
        joystick2.init()
        tanque4_joystick2 = Tank(AMARELO, tela_largura - 150, 2 * tela_altura // 3, {'joystick': joystick2})
        todos_sprites.add(tanque4_joystick2)

    while True:  # Loop principal do jogo
        for evento in pygame.event.get():#Itera sobre todos os eventos do pygame
            if evento.type == pygame.QUIT:#Verifica se o evento é um pedido de sair do jogo
                pygame.quit() #Encerra os módulos do pygame corretamente.
                sys.exit()#Encerra o programa

        todos_sprites.update()#Atualiza todos os sprites do jogo

        tela.fill(PRETO)#Preenche a tela com a cor preta
        todos_sprites.draw(tela)#Desenha todos os sprites na tela

        pygame.display.flip()#Atualiza a tela visível para o usuário

        pygame.time.Clock().tick(60)#Limita ritmo de execução do jogo a 60 quadros por segundo

if __name__ == "__main__":
    main()#Chama a função principal do programa