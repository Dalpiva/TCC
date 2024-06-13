import pygame

# Imports Locais
from .bola import Bola
from .raquete import Raquete

pygame.init()


class Informacao_Jogo:
    def __init__(self, acertos_esq, acertos_dir, pontuacao_esq, pontuacao_dir):
        self.acertos_esq = acertos_esq
        self.acertos_dir = acertos_dir
        self.pontuacao_esq = pontuacao_esq
        self.pontuacao_dir = pontuacao_dir


class Jogo:
    FONTE_PONTUACAO = pygame.font.SysFont("Arial", 50)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)

    def __init__(self, tela, largura_tela, altura_tela):
        self.altura_tela = altura_tela
        self.largura_tela = largura_tela

        self.raquete_esquerda = Raquete(10, self.altura_tela // 2 - Raquete.ALTURA // 2)
        self.raquete_direita = Raquete(
            self.largura_tela - 10 - Raquete.LARGURA,
            self.altura_tela // 2 - Raquete.ALTURA // 2,
        )
        self.bola = Bola(self.largura_tela // 2, self.altura_tela // 2)

        self.pontuacao_esq = 0
        self.pontuacao_dir = 0
        self.acertos_esq = 0
        self.acertos_dir = 0

        self.tela = tela

    def pontuacao(self):
        texto_esquerda = self.FONTE_PONTUACAO.render(
            f"{self.pontuacao_esq}", 1, self.BRANCO
        )
        texto_direita = self.FONTE_PONTUACAO.render(
            f"{self.pontuacao_dir}", 1, self.BRANCO
        )

        self.tela.blit(
            texto_esquerda,
            (self.largura_tela // 4 - texto_esquerda.get_width() // 2, 20),
        )
        self.tela.blit(
            texto_direita,
            (self.largura_tela * 3 // 4 - texto_direita.get_width() // 2, 20),
        )

    def acertos(self):
        texto_acertos = self.FONTE_PONTUACAO.render(
            f"{self.acertos_esq + self.acertos_dir}", 1, self.BRANCO
        )
        self.tela.blit(
            texto_acertos,
            (self.largura_tela // 2 - texto_acertos.get_width() // 2, 10),
        )

    def divisoria(self):
        for i in range(80, self.altura_tela, self.altura_tela // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.tela,
                self.BRANCO,
                (self.largura_tela // 2 - 5, i, 10, self.largura_tela // 20),
            )

    def colisao(self, treino_qlearning=False):
        bola = self.bola
        raquete_esquerda = self.raquete_esquerda
        raquete_direita = self.raquete_direita

        # Paredes
        if bola.y + bola.RAIO >= self.altura_tela:
            bola.vel_y *= -1
        elif bola.y - bola.RAIO <= 0:
            bola.vel_y *= -1

        if treino_qlearning and (bola.x + bola.RAIO >= self.largura_tela - 30):
            bola.vel_x *= -1

        # Esquerda
        if bola.vel_x < 0:
            if (
                bola.y >= raquete_esquerda.y
                and bola.y <= raquete_esquerda.y + Raquete.ALTURA
            ):
                if bola.x - bola.RAIO <= raquete_esquerda.x + Raquete.LARGURA:
                    bola.vel_x *= -1

                    # Logica para o mudanca do Y, desta forma ha uma forma dos jogadores
                    # controlarem a bola
                    # Caso a bola acerte a metade de cima da raquete, ira para cima
                    # Caso a bola acerte a metade de baixo da raquete, ira para baixo
                    meio_y = raquete_esquerda.y + Raquete.ALTURA // 2
                    diferenca_y = meio_y - bola.y

                    fator_de_reducao = (Raquete.ALTURA / 2) / bola.VEL_MAX
                    velocidade_y = diferenca_y / fator_de_reducao
                    bola.vel_y = -1 * velocidade_y
                    self.acertos_esq += 1
        # Direita
        else:
            if (
                bola.y >= raquete_direita.y
                and bola.y <= raquete_direita.y + Raquete.ALTURA
            ):
                if bola.x + bola.RAIO >= raquete_direita.x:
                    bola.vel_x *= -1

                    meio_y = raquete_direita.y + Raquete.ALTURA // 2
                    diferenca_y = meio_y - bola.y

                    fator_de_reducao = (Raquete.ALTURA / 2) / bola.VEL_MAX
                    velocidade_y = diferenca_y / fator_de_reducao
                    bola.vel_y = -1 * velocidade_y
                    self.acertos_dir += 1

    def cria_tela(self, pontuacao=True, acertos=False):
        self.tela.fill(self.PRETO)

        self.divisoria()

        if pontuacao:
            self.pontuacao()

        if acertos:
            self.acertos()

        for raquete in [self.raquete_esquerda, self.raquete_direita]:
            raquete.desenha_raquete(self.tela)

        self.bola.desenha_bola(self.tela)

    def move_raquetes(self, esquerda=True, cima=True):
        if esquerda:
            if cima and self.raquete_esquerda.y - Raquete.VELOCIDADE < 0:
                return False

            if not cima and self.raquete_esquerda.y + Raquete.ALTURA > self.altura_tela:
                return False

            self.raquete_esquerda.move(cima)
        else:
            if cima and self.raquete_direita.y - Raquete.VELOCIDADE < 0:
                return False
            if not cima and self.raquete_direita.y + Raquete.ALTURA > self.altura_tela:
                return False

            self.raquete_direita.move(cima)

        return True

    def loop(self, treino_qlearning=False):
        self.bola.move()
        self.colisao(treino_qlearning)

        if self.bola.x < 0:
            self.pontuacao_dir += 1
            self.bola.reset()
        elif self.bola.x > self.largura_tela:
            self.pontuacao_esq += 1
            self.bola.reset()

        inforamcao_jogo = Informacao_Jogo(
            self.acertos_esq, self.acertos_dir, self.pontuacao_esq, self.pontuacao_dir
        )

        return inforamcao_jogo

    def reset(self):
        self.bola.reset()
        self.raquete_esquerda.reset()
        self.raquete_direita.reset()

        self.pontuacao_esq = 0
        self.pontuacao_dir = 0
        self.acertos_esq = 0
        self.acertos_dir = 0
