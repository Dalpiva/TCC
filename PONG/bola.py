import pygame
import math
import random
from typing import List, Tuple


class Bola:
    VEL_MAX = 5
    RAIO = 8
    COR = (255, 255, 255)

    def __init__(self, x: int, y: int) -> None:
        """
        Inicializa a bola com a posição original e define sua velocidade inicial.

        Args:
            x (int): Posição inicial X da bola.
            y (int): Posição inicial Y da bola.
        """
        self.x = self.x_original = x
        self.y = self.y_original = y
        angulo = self._get_random_angle(-30, 30, [0])
        self.vel_x = abs(math.cos(angulo) * self.VEL_MAX)
        self.vel_y = math.sin(angulo) * self.VEL_MAX

    def _get_random_angle(
        self, angulo_min: int, angulo_max: int, excluded: List[int]
    ) -> float:
        """
        Gera um ângulo aleatório para o movimento da bola, evitando os ângulos excluídos.

        Args:
            angulo_min (int): O ângulo mínimo que a bola pode ter (em graus).
            angulo_max (int): O ângulo máximo que a bola pode ter (em graus).
            excluded (List[int]): Lista de ângulos excluídos.

        Retorna:
            float: O ângulo gerado em radianos.
        """
        angulo = 0
        while angulo in excluded:
            angulo = math.radians(random.randrange(angulo_min, angulo_max))

        return angulo

    def desenha_bola(self, tela: pygame.Surface) -> None:
        """
        Desenha a bola na tela.

        Args:
            tela (pygame.Surface): A superfície onde a bola será desenhada.
        """
        pygame.draw.circle(tela, self.COR, (self.x, self.y), self.RAIO)

    def move(self) -> None:
        """
        Move a bola de acordo com sua velocidade atual.
        """
        self.x += self.vel_x
        self.y += self.vel_y

    def reset(self) -> None:
        """
        Reseta a posição da bola para sua posição original e redefine sua velocidade.
        """
        self.x = self.x_original
        self.y = self.y_original

        angulo = self._get_random_angle(-30, 30, [0])
        self.vel_x = abs(math.cos(angulo) * self.VEL_MAX)
        self.vel_y = math.sin(angulo) * self.VEL_MAX

    def spawn_aleatorio(self, dimensoes: Tuple[int, int]) -> None:
        """
        Coloca a bola em uma posição aleatória na tela e para seu movimento.

        Args:
            dimensoes (Tuple[int, int]): As dimensões da tela (largura, altura).
        """
        self.x = dimensoes[0] // 2 + 50
        self.y = random.randint(50, dimensoes[1] - 50)

        self.vel_x = 0
        self.vel_y = 0
