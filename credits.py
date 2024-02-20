import pygame
import sys

class Credits:
    def __init__(self, largura_tela, altura_tela):
        pygame.init()
        self.tela = pygame.display.set_mode((largura_tela, altura_tela))
        pygame.display.set_caption("Tela de Créditos")

        # Defina as cores
        self.cor_fundo = (89, 164, 89)
        self.cor_branca = (255, 255, 255)
        self.cor_preta = (0, 0, 0)

        # Defina as fontes e tamanhos de texto
        self.fonte_titulo = pygame.font.Font('assets/PressStart2P.ttf', 28)
        self.fonte_credito_nome = pygame.font.Font('assets/PressStart2P.ttf', 10)
        self.fonte_credito_profissao = pygame.font.Font('assets/PressStart2P.ttf', 8)

        # Lista de créditos
        self.creditos = [
            {"nome": "Ana Beatriz Maciel Nunes", "profissao": "Game Developer", "imagem": "assets/ana1.jpg"},
            {"nome": "Fernando Luiz da Silva Freire", "profissao": "Game Developer", "imagem": "assets/fernando1.jpg"},
            {"nome": "Marcelo Heitor de Almeida Lira", "profissao": "Game Developer", "imagem": "assets/marcelo1.jpg"},
        ]

    def exibir_creditos(self):
        self.tela.fill(self.cor_fundo)

        # Título
        texto_titulo = self.fonte_titulo.render("Credits", True, self.cor_branca)
        self.tela.blit(texto_titulo, (self.tela.get_width() // 2 - texto_titulo.get_width() // 2, 50))

        # Exibir créditos com imagens
        x_pos = 65
        for credito in self.creditos:
            # Carregar imagem
            imagem = pygame.image.load(credito["imagem"])
            # Redimensionar imagem para 150x150 pixels
            imagem = pygame.transform.scale(imagem, (150, 150))
            # Exibir imagem
            self.tela.blit(imagem, (x_pos, 190))

            # Exibir nome abaixo da imagem (quebrando linhas se necessário)
            palavras_nome = credito["nome"].split()
            linha_atual_nome = ""
            y_pos_nome = 370
            for palavra_nome in palavras_nome:
                linha_teste_nome = linha_atual_nome + palavra_nome + " "
                if self.fonte_credito_nome.render(linha_teste_nome, True, self.cor_branca).get_width() < 200:
                    linha_atual_nome = linha_teste_nome
                else:
                    texto_nome = self.fonte_credito_nome.render(linha_atual_nome, True, self.cor_branca)
                    self.tela.blit(texto_nome, (x_pos + 75 - texto_nome.get_width() // 2, y_pos_nome))
                    linha_atual_nome = palavra_nome + " "
                    y_pos_nome += 20

            # Renderizar a última linha do nome
            texto_nome = self.fonte_credito_nome.render(linha_atual_nome, True, self.cor_branca)
            self.tela.blit(texto_nome, (x_pos + 75 - texto_nome.get_width() // 2, y_pos_nome))

            # Exibir profissao abaixo do nome
            y_pos_profissao = y_pos_nome + 25
            texto_profissao = self.fonte_credito_profissao.render(credito["profissao"], True, self.cor_preta)
            self.tela.blit(texto_profissao, (x_pos + 75 - texto_profissao.get_width() // 2, y_pos_profissao))

            x_pos += 250

        pygame.display.flip()

    def executar(self):
        rodando = True
        while rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False

            self.exibir_creditos()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    tela_creditos = Credits(800, 600)
    tela_creditos.executar()
