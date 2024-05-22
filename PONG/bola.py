import pygame
import math
import random


class Bola:
    VEL_MAX = 5
    RAIO = 8
    COR = (255, 255, 255)

    def __init__(self, x, y):
        self.x = self.x_original = x
        self.y = self.y_original = y
        angulo = self._get_random_angle(-30, 30, [0])
        self.vel_x = -abs(math.cos(angulo) * self.VEL_MAX)
        self.vel_y = math.sin(angulo) * self.VEL_MAX

    def _get_random_angle(self, angulo_min, angulo_max, excluded):
        angulo = 0
        while angulo in excluded:
            angulo = math.radians(random.randrange(angulo_min, angulo_max))

        return angulo

    def desenha_bola(self, tela):
        pygame.draw.circle(tela, self.COR, (self.x, self.y), self.RAIO)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def reset(self):
        self.x = self.x_original
        self.y = self.y_original

        angulo = self._get_random_angle(-30, 30, [0])
        vel_x = abs(math.cos(angulo) * self.VEL_MAX)
        vel_y = math.sin(angulo) * self.VEL_MAX

        self.vel_x = -vel_x
        self.vel_y = vel_y
