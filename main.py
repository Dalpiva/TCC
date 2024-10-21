# Referencia
# https://github.com/techwithtim/Pong-Python
# https://github.com/techwithtim/NEAT-Pong-Python

import pygame


from NeuralNetwork import ArtificialNeuralNetwork
from QLearning import QLearning
from PongGame import PongGame

from treino_rna import treinamento_ann
from treino_ql import treinamento_q_learning

LARGURA, ALTURA = 700, 500


def jogar():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Player x Oponente Perfeito")

    jogo = PongGame(tela, LARGURA, ALTURA)
    jogo.jogar()


def jogar_ann(geracao):
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Redes Neurais Artificiais")

    jogo = PongGame(tela, LARGURA, ALTURA)

    vencedor = ArtificialNeuralNetwork.carrega_individuo(geracao=geracao)

    jogo.jogar_ann(individuo=vencedor)


def jogar_q_learning():
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning.carrega_melhor()

    jogo.jogar_qlearning(agente=agente)


if __name__ == "__main__":
    # jogar()
    # treinamento_ann()
    # jogar_ann(geracao=1)
    # treinamento_q_learning()
    jogar_q_learning()
