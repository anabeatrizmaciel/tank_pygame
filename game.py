import pygame
import sys
from tank import Tank
from maze import Maze
from color import Color
from list import selected_maze
from bonus import Bonus  # Importing Bonus class

class Game:
    def __init__(self):
        pygame.init()
        screen_width = 800
        screen_height = 600
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.color = Color()

        self.maze = Maze(screen_width, screen_height, self.color, selected_maze)
        self.maze.create_walls_group()

        self.bullets = pygame.sprite.Group()

        image_path_tank_1 = "assets/tanque1_spritesheet.png"
        image_path_tank_2 = "assets/tanque2_spritesheet.png"
        image_path_tank_3 = "assets/tanque3.png"
        image_path_tank_4 = "assets/tanque4.png"

        self.tank1 = Tank((255, 255, 255), 150, screen_height // 3, 1, {
            'teclas': {'cima': pygame.K_w, 'baixo': pygame.K_s, 'esquerda': pygame.K_a, 'direita': pygame.K_d,
                       'disparar': pygame.K_SPACE}}, self.bullets, screen_width, screen_height, self.maze.walls,
                        spritesheet_path=image_path_tank_1)

        self.tank2 = Tank((0, 0, 0), screen_width - 150, screen_height // 3, 2, {
            'teclas': {'cima': pygame.K_UP, 'baixo': pygame.K_DOWN, 'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT,
                       'disparar': pygame.K_RETURN}}, self.bullets, screen_width, screen_height, self.maze.walls,
                        spritesheet_path=image_path_tank_2)

        self.tank1.direction = "right"
        self.tank2.direction = "left"

        self.tank1.set_walls(self.maze.walls)
        self.tank2.set_walls(self.maze.walls)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank1, self.tank2)

        self.tank3_joystick1 = None
        self.tank4_joystick2 = None

        if pygame.joystick.get_count() >= 1:
            joystick1 = pygame.joystick.Joystick(0)
            joystick1.init()
            self.tank3_joystick1 = Tank(self.color.BLUE, 150, 2 * screen_height // 3, {'joystick': joystick1},
                                           self.bullets, screen_width, screen_height, self.maze.walls, image_path_tank_3)
            self.tank3_joystick1.set_walls(self.maze.walls)
            self.all_sprites.add(self.tank3_joystick1)

        if pygame.joystick.get_count() >= 2:
            joystick2 = pygame.joystick.Joystick(1)
            joystick2.init()
            self.tank4_joystick2 = Tank(self.color.YELLOW, screen_width - 150, 2 * screen_height // 3,
                                           {'joystick': joystick2}, self.bullets, screen_width, screen_height, self.maze.walls, image_path_tank_4,
                                           [self.tank1, self.tank2, self.tank3_joystick1 if pygame.joystick.get_count() >= 1 else None])
            self.tank4_joystick2.set_walls(self.maze.walls)
            self.all_sprites.add(self.tank4_joystick2)

        pygame.font.init()
        self.font = pygame.font.Font('assets/PressStart2P.ttf', 15)

        # Initialize sprite group for the bonus
        self.bonuses = pygame.sprite.Group()
        self.next_bonus_time = pygame.time.get_ticks() + 50000  # Time, in milliseconds to the next bonus (30 seconds)

    def generate_bonus(self):
        bonus = Bonus()
        bonus.generate_position(self.screen.get_width(), self.screen.get_height(), self.maze.walls)
        self.bonuses.add(bonus)

    def draw_score(self):
        y_offset = 10
        for tank in [self.tank1, self.tank2, self.tank3_joystick1, self.tank4_joystick2]:
            if tank is not None:
                score_text = self.font.render(f"Tank {tank.id} Life: {tank.lives}", True, (255, 255, 255))
                self.screen.blit(score_text, (10, y_offset))
                y_offset += 20

    def check_winner(self):
        tanks_alive = [tank for tank in [self.tank1, self.tank2, self.tank3_joystick1, self.tank4_joystick2] if tank is not None and tank.alive()]
        if len(tanks_alive) == 1:
            return tanks_alive[0].id
        return None

    def show_winner_screen(self, winner_id):
        self.screen.fill(self.color.BLACK)

        winner_text = self.font.render(f"Tank {winner_id} Won!", True, (255, 255, 255))
        text_rect = winner_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(winner_text, text_rect)

        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            # If the current time is greater or equal to the time for the next bonus, generate bonus
            if current_time >= self.next_bonus_time:
                self.generate_bonus()
                # Define next bonus spawn for 30 seconds
                self.next_bonus_time = current_time + 50000

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.tank1.fire_bullet(self.tank1.direction, [self.tank2, self.tank3_joystick1, self.tank4_joystick2])
                    elif evento.key == pygame.K_RETURN:
                        self.tank2.fire_bullet(self.tank2.direction, [self.tank1, self.tank3_joystick1, self.tank4_joystick2])

                elif evento.type == pygame.JOYBUTTONDOWN:
                    if evento.joy == 0:
                        self.tank3_joystick1.fire_bullet(self.tank3_joystick1.direction, None)
                    elif evento.joy == 1:
                        self.tank4_joystick2.fire_bullet(self.tank4_joystick2.direction, None)

            self.bullets.update()
            self.all_sprites.update()

            # Verify collisions between the tanks and the bonuses
            bonus_collisions = pygame.sprite.groupcollide(self.bonuses, self.all_sprites, True, False)
            for bonus, tanks in bonus_collisions.items():
                for tank in tanks:
                    tank.increment_lives()  # Increase the life of the tank that collided with the bonus

            winner_id = self.check_winner()
            if winner_id is not None:
                self.show_winner_screen(winner_id)
                break

            self.screen.fill(self.color.BLACK)
            self.maze.draw(self.screen)
            self.bullets.draw(self.screen)
            self.all_sprites.draw(self.screen)
            self.bonuses.draw(self.screen)  # Draw bonus in the screen
            self.draw_score()

            pygame.display.flip()
            pygame.time.Clock().tick(60)
