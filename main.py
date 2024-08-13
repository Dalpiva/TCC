# Referencia

# https://github.com/techwithtim/Pong-Python
# https://github.com/techwithtim/NEAT-Pong-Python

from PONG import Jogo
from NeuralNetwork import ArtificialNeuralNetwork
from QLearning import QLearning

import pygame
import pickle
import numpy as np


class PongGame:
    def __init__(self, tela, largura, altura):
        self.jogo = Jogo(tela, largura, altura)
        self.bola = self.jogo.bola
        self.raquete_esquerda = self.jogo.raquete_esquerda
        self.raquete_direita = self.jogo.raquete_direita

    def jogada_adversario_perfeito(self):
        acao = self.jogo.adversario_perfeito()
        if acao:
            self.jogo.move_raquetes(esquerda=False, cima=True)
        else:
            self.jogo.move_raquetes(esquerda=False, cima=False)

    def jogar(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Acertos da IA: ", informacao_jogo.acertos_dir)
                    run = False
                    break

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_w]:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            if teclas[pygame.K_s]:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            self.jogada_adversario_perfeito()

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()

    def testa_ia(self, individuo):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Acertos da IA: ", informacao_jogo.acertos_dir)
                    run = False
                    break

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_w]:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            if teclas[pygame.K_s]:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            entrada = individuo.cria_entrada(
                raquete_y=self.raquete_direita.y,
                bola_y=self.bola.y,
                distancia_bola=abs(self.raquete_direita.x - self.bola.x),
            )

            decisao = individuo.calcula_saida(
                input=entrada, nos=individuo.nos, pesos=individuo.pesos
            )

            if decisao == 0:
                pass
            elif decisao == 1:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()

    def treina_ann(self, individuo_1, individuo_2):
        run = True
        # clock = pygame.time.Clock()

        while run:
            # clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            entrada_1 = individuo_1.cria_entrada(
                raquete_y=self.raquete_esquerda.y,
                bola_y=self.bola.y,
                distancia_bola=abs(self.raquete_esquerda.x - self.bola.x),
            )
            decisao_1 = individuo_1.calcula_saida(
                input=entrada_1, nos=individuo_1.nos, pesos=individuo_1.pesos
            )
            if decisao_1 == 0:
                pass
            elif decisao_1 == 1:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            entrada_2 = individuo_2.cria_entrada(
                raquete_y=self.raquete_direita.y,
                bola_y=self.bola.y,
                distancia_bola=abs(self.raquete_direita.x - self.bola.x),
            )
            decisao_2 = individuo_2.calcula_saida(
                input=entrada_2, nos=individuo_2.nos, pesos=individuo_2.pesos
            )

            if decisao_2 == 0:
                pass
            elif decisao_2 == 1:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            informacao_jogo = self.jogo.loop(treino_qlearning=True)
            self.jogo.cria_tela(False, True)
            pygame.display.update()

            # Se alguem errar, para o jogo
            if (
                informacao_jogo.pontuacao_dir >= 1
                or informacao_jogo.pontuacao_esq >= 1
                or informacao_jogo.acertos_esq > 50
            ):
                self.calcula_fitness(
                    individuo_1=individuo_1,
                    individuo_2=individuo_2,
                    informacao_jogo=informacao_jogo,
                )
                run = False

        # pygame.quit()

    def calcula_fitness(self, individuo_1, individuo_2, informacao_jogo):
        individuo_1.fitness += informacao_jogo.acertos_esq
        individuo_2.fitness += informacao_jogo.acertos_dir

    """def treina_qlearning(self, agente):
        run = True
        # clock = pygame.time.Clock()

        while run:
            # clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            if decisao_1 == 0:
                pass
            elif decisao_1 == 1:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            entrada_2 = individuo_2.cria_entrada(
                raquete_y=self.raquete_direita.y,
                bola_y=self.bola.y,
                distancia_bola=abs(self.raquete_direita.x - self.bola.x),
            )
            decisao_2 = individuo_2.calcula_saida(
                input=entrada_2, nos=individuo_2.nos, pesos=individuo_2.pesos
            )

            if decisao_2 == 0:
                pass
            elif decisao_2 == 1:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            informacao_jogo = self.jogo.loop(treino_qlearning=True)
            self.jogo.cria_tela(False, True)
            pygame.display.update()

            # Se alguem errar, para o jogo
            if (
                informacao_jogo.pontuacao_dir >= 1
                or informacao_jogo.pontuacao_esq >= 1
                or informacao_jogo.acertos_esq > 50
            ):
                self.calcula_fitness(
                    individuo_1=individuo_1,
                    individuo_2=individuo_2,
                    informacao_jogo=informacao_jogo,
                )
                run = False

        # pygame.quit()"""


def ia_x_ia_ann():
    populacao = 100
    geracoes = 10

    individuos = []
    for i in range(populacao):
        individuos.append(ArtificialNeuralNetwork(3, 3))

    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - IA x IA - ANN")

    print("Iniciando treinamento - ANN!")

    for geracao in range(geracoes):
        print(f"Geracao {geracao+1} ###########################")
        for i in range(len(individuos)):
            # for j in range(len(individuos)):
            # print(f"Jogo entre individuo_{i} e individuo_{i}")
            jogo = PongGame(tela, LARGURA, ALTURA)
            jogo.treina_ann(individuo_1=individuos[i], individuo_2=individuos[i])
            # print("Jogo Finalizado!")

            # print(f"Fitness individuo_{i}: ", individuos[i].fitness)
            # print(f"Fitness individuo_{j}: ", individuos[j].fitness)

            # print("")

        t1 = ArtificialNeuralNetwork.melhor_individuo(individuos=individuos)
        with open(f"geracoes/melhor_individuo_geracao_{geracao}.pickle", "wb") as f:
            pickle.dump(t1, f)

        individuos = ArtificialNeuralNetwork.mutacao(top1=t1, individuos=individuos)


def player_conta_ia(q_learning=False, geracao=1):
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Player x IA")

    jogo = PongGame(tela, LARGURA, ALTURA)

    if not q_learning:
        with open(f"geracoes/melhor_individuo_geracao_{geracao-1}.pickle", "rb") as f:
            vencedor = pickle.load(f)
        jogo.testa_ia(individuo=vencedor)
    else:
        with open("QLearning/ia.pickle", "rb") as f:
            vencedor = pickle.load(f)

        jogo.testa_q(qlearning=vencedor)


def jogar():
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Player x Oponente Perfeito")

    jogo = PongGame(tela, LARGURA, ALTURA)
    jogo.jogar()


def treinamento_q_learning():
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Treinamento Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning()

    jogo.treina_qlearning(agente=agente)


if __name__ == "__main__":
    # player_conta_ia(geracao=3)
    # ia_x_ia_ann()
    # ia_x_ia_qlearning()
    # player_conta_ia(q_learning=True)
    jogar()
