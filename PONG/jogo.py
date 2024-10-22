import pygame

# Imports Locais
from .bola import Bola
from .raquete import Raquete

pygame.init()


class InformacaoJogo:
    def __init__(
        self, acertos_esq: int, acertos_dir: int, pontuacao_esq: int, pontuacao_dir: int
    ) -> None:
        """
        Inicializa a classe com as informações do jogo, incluindo pontuações e acertos.

        Args:
            acertos_esq (int): Número de acertos da raquete esquerda.
            acertos_dir (int): Número de acertos da raquete direita.
            pontuacao_esq (int): Pontuação da raquete esquerda.
            pontuacao_dir (int): Pontuação da raquete direita.
        """
        self.acertos_esq = acertos_esq
        self.acertos_dir = acertos_dir
        self.pontuacao_esq = pontuacao_esq
        self.pontuacao_dir = pontuacao_dir


class Jogo:
    FONTE_PONTUACAO = pygame.font.SysFont("Arial", 50)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)

    def __init__(
        self, tela: pygame.Surface, largura_tela: int, altura_tela: int
    ) -> None:
        """
        Inicializa o jogo com a tela, raquetes, bola e pontuações.

        Args:
            tela (pygame.Surface): Superfície do jogo.
            largura_tela (int): Largura da tela.
            altura_tela (int): Altura da tela.
        """
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

    def pontuacao(self) -> None:
        """
        Exibe a pontuação das raquetes na tela.
        """
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

    def acertos(self) -> None:
        """
        Exibe o número total de acertos (esquerda e direita) na tela.
        """
        texto_acertos = self.FONTE_PONTUACAO.render(
            f"{self.acertos_esq + self.acertos_dir}", 1, self.BRANCO
        )
        self.tela.blit(
            texto_acertos,
            (self.largura_tela // 2 - texto_acertos.get_width() // 2, 10),
        )

    def divisoria(self) -> None:
        """
        Desenha uma linha divisória no meio da tela.
        """
        for i in range(80, self.altura_tela, self.altura_tela // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.tela,
                self.BRANCO,
                (self.largura_tela // 2 - 5, i, 10, self.largura_tela // 20),
            )

    def colisao(self) -> None:
        """
        Detecta e lida com colisões da bola com as raquetes e as paredes.
        """
        bola = self.bola
        raquete_esquerda = self.raquete_esquerda
        raquete_direita = self.raquete_direita

        # Paredes
        if bola.y + bola.RAIO >= self.altura_tela:
            bola.vel_y *= -1
        elif bola.y - bola.RAIO <= 0:
            bola.vel_y *= -1

        # Esquerda
        if bola.vel_x < 0:
            if (
                bola.y >= raquete_esquerda.y
                and bola.y <= raquete_esquerda.y + Raquete.ALTURA
            ):
                if bola.x - bola.RAIO <= raquete_esquerda.x + Raquete.LARGURA:
                    bola.vel_x *= -1
                    meio_y = raquete_esquerda.y + Raquete.ALTURA // 2
                    diferenca_y = meio_y - bola.y

                    fator_de_reducao = (Raquete.ALTURA / 2) / bola.VEL_MAX
                    bola.vel_y = -1 * (diferenca_y / fator_de_reducao)
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
                    bola.vel_y = -1 * (diferenca_y / fator_de_reducao)
                    self.acertos_dir += 1

    def cria_tela(self, pontuacao: bool = True, acertos: bool = False) -> None:
        """
        Cria a tela do jogo com as raquetes, bola e, opcionalmente, as pontuações e acertos.

        Args:
            pontuacao (bool, opcional): Exibe a pontuação se True. Padrão é True.
            acertos (bool, opcional): Exibe os acertos se True. Padrão é False.
        """
        self.tela.fill(self.PRETO)

        self.divisoria()

        if pontuacao:
            self.pontuacao()

        if acertos:
            self.acertos()

        for raquete in [self.raquete_esquerda, self.raquete_direita]:
            raquete.desenha_raquete(self.tela)

        self.bola.desenha_bola(self.tela)

    def move_raquetes(self, esquerda: bool = True, cima: bool = True) -> bool:
        """
        Move as raquetes para cima ou para baixo, dependendo da direção.

        Args:
            esquerda (bool, opcional): Mover a raquete esquerda se True, caso contrário mover a direita. Padrão é True.
            cima (bool, opcional): Mover a raquete para cima se True, caso contrário para baixo. Padrão é True.

        Retorna:
            bool: Retorna False se a raquete não puder se mover (limites da tela), caso contrário True.
        """
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

    def loop(self) -> InformacaoJogo:
        """
        Executa o loop principal do jogo, movendo a bola e verificando colisões.

        Retorna:
            InformacaoJogo: Objeto contendo o estado atual do jogo (acertos e pontuações).
        """
        self.bola.move()
        self.colisao()

        if self.bola.x < 0:
            self.pontuacao_dir += 1
            self.bola.reset()
        elif self.bola.x > self.largura_tela:
            self.pontuacao_esq += 1
            self.bola.reset()

        return InformacaoJogo(
            self.acertos_esq, self.acertos_dir, self.pontuacao_esq, self.pontuacao_dir
        )

    def reset(self) -> None:
        """
        Reseta o jogo para o estado inicial, incluindo as posições e pontuações.
        """
        self.bola.reset()
        self.raquete_esquerda.reset()
        self.raquete_direita.reset()

        self.pontuacao_esq = 0
        self.pontuacao_dir = 0
        self.acertos_esq = 0
        self.acertos_dir = 0

    def adversario_perfeito(self) -> bool:
        """
        Controla a raquete direita como um adversário perfeito, seguindo a posição da bola.

        Retorna:
            bool: Retorna True se a bola está acima da raquete, False se está abaixo.
        """
        centro_y_raquete = self.raquete_direita.y + self.raquete_direita.ALTURA // 2

        if self.bola.y < centro_y_raquete:
            return True  # A bola está acima
        else:
            return False  # A bola está abaixo
