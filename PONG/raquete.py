import pygame


class Raquete:
    COR = (255, 255, 255)
    VELOCIDADE = 4
    LARGURA = 20
    ALTURA = 100

    def __init__(self, x, y):
        self.x = self.x_original = x
        self.y = self.y_original = y

    def desenha_raquete(self, tela):
        pygame.draw.rect(tela, self.COR, (self.x, self.y, self.LARGURA, self.ALTURA))

    def move(self, cima=True):
        if cima:
            self.y -= self.VELOCIDADE
        else:
            self.y += self.VELOCIDADE

    def reset(self):
        self.x = self.x_original
        self.y = self.y_original
