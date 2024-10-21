import pygame
from time import time
from QLearning import QLearning
from PongGame import PongGame

LARGURA, ALTURA = 700, 500


def treinamento_q_learning(episodios=500, desconto=0.0001, alpha=0.4, gamma=0.9):
    inicio = time()

    tela = pygame.display.set_mode((LARGURA, ALTURA))

    pygame.display.set_caption("PONG - TCC WESLEY - Treinamento Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning(desconto, alpha, gamma)

    for i in range(episodios):
        jogo.bola.spawn_aleatorio((LARGURA, ALTURA))
        agente.acoes = 0
        jogo.treina_qlearning(agente=agente)

        if i % 10 == 0:
            QLearning.salva_agente(episodio=i, agente=agente)

        print(f"Episodio {i+1}, Epsilon: {agente.epsilon}, recompensa: {agente.acoes}")

    tempo_decorrido = round(time() - inicio, 2)
    agente.tempo_treino = tempo_decorrido

    QLearning.salva_final(agente=agente)

    print("Treinamento Finalizado - QLearning!")
