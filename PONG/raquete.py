import pygame


class Raquete:
    COR = (255, 255, 255)
    VELOCIDADE = 4
    LARGURA = 20
    ALTURA = 100

    def __init__(self, x: int, y: int) -> None:
        """
        Inicializa a raquete com sua posição original.

        Args:
            x (int): Posição X da raquete.
            y (int): Posição Y da raquete.
        """
        self.x = self.x_original = x
        self.y = self.y_original = y

    def desenha_raquete(self, tela: pygame.Surface) -> None:
        """
        Desenha a raquete na tela.

        Args:
            tela (pygame.Surface): A superfície onde a raquete será desenhada.
        """
        pygame.draw.rect(tela, self.COR, (self.x, self.y, self.LARGURA, self.ALTURA))

    def move(self, cima: bool = True) -> None:
        """
        Move a raquete para cima ou para baixo dependendo da direção.

        Args:
            cima (bool, opcional): Mover para cima se True, ou para baixo se False. Padrão é True.
        """
        if cima:
            self.y -= self.VELOCIDADE
        else:
            self.y += self.VELOCIDADE

    def reset(self) -> None:
        """
        Reseta a posição da raquete para sua posição original.
        """
        self.x = self.x_original
        self.y = self.y_original
