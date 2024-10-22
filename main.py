# Referências:
#     https://github.com/techwithtim/Pong-Python
#     https://github.com/techwithtim/NEAT-Pong-Python

# Dependências:
#     - pygame: Biblioteca para desenvolvimento de jogos.

import pygame
from NeuralNetwork import ArtificialNeuralNetwork
from QLearning import QLearning
from PongGame import PongGame
from treino_ann import treinar_rede_neural_artificial
from treino_ql import treinar_q_learning

# Definindo a largura e altura da tela do jogo
LARGURA, ALTURA = 700, 500


def iniciar_jogo_normal() -> None:
    """
    Inicia uma partida de Pong entre o jogador e um oponente controlado pelo computador.

    A função cria uma janela de jogo e utiliza a classe `PongGame` para rodar o jogo.
    O jogador controla uma das raquetes, enquanto a outra é controlada pelo computador.
    """
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Player x Oponente Perfeito")

    jogo = PongGame(tela, LARGURA, ALTURA)
    jogo.jogar()


def iniciar_jogo_com_ann() -> None:
    """
    Inicia uma partida de Pong usando um modelo de Rede Neural Artificial treinado.

    A função carrega o indivíduo da geração especificada e utiliza a classe `PongGame`
    para rodar o jogo, onde o indivíduo controlado pela RNA joga contra o jogador.
    """
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Redes Neurais Artificiais")

    jogo = PongGame(tela, LARGURA, ALTURA)

    individuo = ArtificialNeuralNetwork.carrega_melhor()

    jogo.jogar_com_ann(individuo=individuo)


def iniciar_jogo_com_q_learning() -> None:
    """
    Inicia uma partida de Pong utilizando um agente treinado com Q-Learning.

    A função carrega o melhor agente treinado via Q-Learning e utiliza a classe `PongGame`
    para rodar o jogo, onde o agente joga contra o jogador.
    """
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning.carrega_melhor()

    jogo.jogar_com_qlearning(agente=agente)


if __name__ == "__main__":
    # iniciar_jogo_normal()
    treinar_rede_neural_artificial()
    # iniciar_jogo_com_ann(geracao=1)
    # treinar_q_learning()
    # iniciar_jogo_com_q_learning()
