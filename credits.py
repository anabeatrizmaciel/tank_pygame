import pygame
import sys

class Credits:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tela de Créditos")

        # Defining colors
        self.BACKGROUND = (89, 164, 89)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Defining text fonts and size
        self.font_title = pygame.font.Font('assets/PressStart2P.ttf', 28)
        self.font_credits_name = pygame.font.Font('assets/PressStart2P.ttf', 10)
        self.font_credits_job = pygame.font.Font('assets/PressStart2P.ttf', 8)

        # Credits list
        self.credits = [
            {"nome": "Ana Beatriz Maciel Nunes", "profissao": "Game Developer", "imagem": "assets/ana1.jpg"},
            {"nome": "Fernando Luiz da Silva Freire", "profissao": "Game Developer", "imagem": "assets/fernando1.jpg"},
            {"nome": "Marcelo Heitor de Almeida Lira", "profissao": "Game Developer", "imagem": "assets/marcelo1.jpg"},
        ]

    def show_credits(self):
        self.screen.fill(self.BACKGROUND)

        # Title
        text_title = self.font_title.render("Credits", True, self.WHITE)
        self.screen.blit(text_title, (self.screen.get_width() // 2 - text_title.get_width() // 2, 50))

        # Show credits images
        x_pos = 65
        for credit in self.credits:
            # Load image
            image = pygame.image.load(credit["imagem"])
            # Re-dimension image to 150x150 pixels
            image = pygame.transform.scale(image, (150, 150))
            # Show image
            self.screen.blit(image, (x_pos, 190))

            # Show name below image (breaking the lines, if necessary)
            name_words = credit["nome"].split()
            current_line_name = ""
            y_pos_nome = 370
            for name_word in name_words:
                test_line_name = current_line_name + name_word + " "
                if self.font_credits_name.render(test_line_name, True, self.WHITE).get_width() < 200:
                    current_line_name = test_line_name
                else:
                    text_name = self.font_credits_name.render(current_line_name, True, self.WHITE)
                    self.screen.blit(text_name, (x_pos + 75 - text_name.get_width() // 2, y_pos_nome))
                    current_line_name = name_word + " "
                    y_pos_nome += 20

            # Render last line of the name
            text_name = self.font_credits_name.render(current_line_name, True, self.WHITE)
            self.screen.blit(text_name, (x_pos + 75 - text_name.get_width() // 2, y_pos_nome))

            # Show job below the name
            y_pos_job = y_pos_nome + 25
            text_job = self.font_credits_job.render(credit["profissao"], True, self.BLACK)
            self.screen.blit(text_job, (x_pos + 75 - text_job.get_width() // 2, y_pos_job))

            x_pos += 250

        pygame.display.flip()

    def execute(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.show_credits()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    credits_screen = Credits(800, 600)
    credits_screen.execute()
