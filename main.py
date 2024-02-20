import pygame
import sys
from game import Game
from credits import Credits

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tela de Início")

background_image = pygame.image.load("assets/tela_inicial.png")
background_rect = background_image.get_rect()

big_font = pygame.font.Font('assets/PressStart2P.ttf', 36)
small_font = pygame.font.Font('assets/PressStart2P.ttf', 20)

credits_screen = Credits(screen_width, screen_height)


def show_credits():
    credits_screen.executar()


def start_game():
    game = Game()
    game.run()


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    start_game()
                elif credits_button_rect.collidepoint(mouse_pos):
                    show_credits()

        screen.fill(BLACK)
        screen.blit(background_image, background_rect)

        combat_text = big_font.render("Combat", True, WHITE)
        combat_rect = combat_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(combat_text, combat_rect)

        play_text = small_font.render("Play", True, WHITE)
        play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(play_text, play_rect)

        credits_button_text = small_font.render("Credits", True, WHITE)
        credits_button_rect = credits_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(credits_button_text, credits_button_rect)

        # Armazene as referências para os botões para verificar cliques posteriormente
        play_button_rect = play_rect

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
