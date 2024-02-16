import pygame
import sys
from tank import Tank
from maze import Maze
from color import Color
from list import labirinto_escolhido
from bonus import Bonus  # Importe a classe Bonus

class Game:
    def __init__(self):
        pygame.init()
        tela_largura = 800
        tela_altura = 600
        self.tela = pygame.display.set_mode((tela_largura, tela_altura))
        self.color = Color()

        self.maze = Maze(tela_largura, tela_altura, self.color, labirinto_escolhido)
        self.maze.create_walls_group()

        self.bullets = pygame.sprite.Group()

        self.tanque1 = Tank((255, 255, 255), 150, tela_altura // 3, 1, {
            'teclas': {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d,
                       'disparar': pygame.K_SPACE}}, self.bullets, tela_largura, tela_altura, self.maze.walls)

        self.tanque2 = Tank((0, 0, 0), tela_largura - 150, tela_altura // 3, 2, {
            'teclas': {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT,
                       'disparar': pygame.K_RETURN}}, self.bullets, tela_largura, tela_altura, self.maze.walls)

        self.tanque1.direction = "right"
        self.tanque2.direction = "left"

        self.tanque1.set_walls(self.maze.walls)
        self.tanque2.set_walls(self.maze.walls)

        self.todos_sprites = pygame.sprite.Group()
        self.todos_sprites.add(self.tanque1, self.tanque2)

        self.tanque3_joystick1 = None
        self.tanque4_joystick2 = None

        if pygame.joystick.get_count() >= 1:
            joystick1 = pygame.joystick.Joystick(0)
            joystick1.init()
            self.tanque3_joystick1 = Tank(self.color.BLUE, 150, 2 * tela_altura // 3, {'joystick': joystick1},
                                           self.bullets, tela_largura, tela_altura, self.maze.walls)
            self.tanque3_joystick1.set_walls(self.maze.walls)
            self.todos_sprites.add(self.tanque3_joystick1)

        if pygame.joystick.get_count() >= 2:
            joystick2 = pygame.joystick.Joystick(1)
            joystick2.init()
            self.tanque4_joystick2 = Tank(self.color.YELLOW, tela_largura - 150, 2 * tela_altura // 3,
                                           {'joystick': joystick2}, self.bullets, tela_largura, tela_altura, self.maze.walls,
                                           [self.tanque1, self.tanque2, self.tanque3_joystick1 if pygame.joystick.get_count() >= 1 else None])
            self.tanque4_joystick2.set_walls(self.maze.walls)
            self.todos_sprites.add(self.tanque4_joystick2)

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

        # Inicialize o grupo de sprites para os bônus
        self.bonuses = pygame.sprite.Group()
        self.next_bonus_time = pygame.time.get_ticks() + 30000  # Tempo em milissegundos para o próximo bônus (30 segundos)

    def generate_bonus(self):
        bonus = Bonus()
        bonus.generate_position(self.tela.get_width(), self.tela.get_height(), self.maze.walls)
        self.bonuses.add(bonus)

    def draw_score(self):
        y_offset = 10
        for tanque in [self.tanque1, self.tanque2, self.tanque3_joystick1, self.tanque4_joystick2]:
            if tanque is not None:
                score_text = self.font.render(f"Tanque {tanque.id} Vidas: {tanque.lives}", True, (255, 255, 255))
                self.tela.blit(score_text, (10, y_offset))
                y_offset += 20

    def check_winner(self):
        tanks_alive = [tank for tank in [self.tanque1, self.tanque2, self.tanque3_joystick1, self.tanque4_joystick2] if tank is not None and tank.alive()]
        if len(tanks_alive) == 1:
            return tanks_alive[0].id
        return None

    def show_winner_screen(self, winner_id):
        self.tela.fill(self.color.BLACK)

        winner_text = self.font.render(f"Tanque {winner_id} Venceu!", True, (255, 255, 255))
        text_rect = winner_text.get_rect(center=(self.tela.get_width() // 2, self.tela.get_height() // 2))
        self.tela.blit(winner_text, text_rect)

        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            # Se o tempo atual for maior ou igual ao tempo para o próximo bônus, gere um novo bônus
            if current_time >= self.next_bonus_time:
                self.generate_bonus()
                # Defina o próximo tempo de bônus para daqui a 30 segundos
                self.next_bonus_time = current_time + 30000

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.tanque1.fire_bullet(self.tanque1.direction, [self.tanque2, self.tanque3_joystick1, self.tanque4_joystick2])
                    elif evento.key == pygame.K_RETURN:
                        self.tanque2.fire_bullet(self.tanque2.direction, [self.tanque1, self.tanque3_joystick1, self.tanque4_joystick2])

                elif evento.type == pygame.JOYBUTTONDOWN:
                    if evento.joy == 0:
                        self.tanque3_joystick1.fire_bullet(self.tanque3_joystick1.direction, None)
                    elif evento.joy == 1:
                        self.tanque4_joystick2.fire_bullet(self.tanque4_joystick2.direction, None)

            self.bullets.update()
            self.todos_sprites.update()

            # Verifica colisões entre cada tanque e o grupo de bônus
            bonus_collisions = pygame.sprite.groupcollide(self.bonuses, self.todos_sprites, True, False)
            for bonus, tanks in bonus_collisions.items():
                for tank in tanks:
                    tank.increment_lives()  # Incrementa a vida de cada tanque que colidiu com o bônus

            winner_id = self.check_winner()
            if winner_id is not None:
                self.show_winner_screen(winner_id)
                break

            self.tela.fill(self.color.BLACK)
            self.maze.draw(self.tela)
            self.bullets.draw(self.tela)
            self.todos_sprites.draw(self.tela)
            self.bonuses.draw(self.tela)  # Desenhe os bônus na tela
            self.draw_score()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

game = Game()
game.run()
