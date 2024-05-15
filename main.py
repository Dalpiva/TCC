# Referencia

# https://github.com/techwithtim/Pong-Python
# https://github.com/techwithtim/NEAT-Pong-Python/blob/main/pong/game.py

from PONG import Jogo

import pygame


class Pong_Game:
    def __init__(self, tela, largura, altura):
        self.jogo = Jogo(tela, largura, altura)
        self.bola = self.jogo.bola
        self.raquete_esquerda = self.jogo.raquete_esquerda
        self.raquete_direita = self.jogo.raquete_direita

    def jogar_pong(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_w]:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            if teclas[pygame.K_s]:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            if teclas[pygame.K_UP]:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            if teclas[pygame.K_DOWN]:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()


def jogar():
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))

    jogo = Pong_Game(tela, LARGURA, ALTURA)
    jogo.jogar_pong()


if __name__ == "__main__":
    jogar()
