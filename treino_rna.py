import pygame
from time import time

from NeuralNetwork import ArtificialNeuralNetwork
from PongGame import PongGame

LARGURA, ALTURA = 700, 500


def ainda_esta_treinando(geracoes_totais, geracao_atual) -> bool:
    if geracoes_totais == -1:
        return True

    if geracao_atual < geracoes_totais:
        return True
    else:
        return False


def treinamento_ann(populacao=100, geracoes=-1, fitness_medio=15, fitness_minimo=5):
    inicio = time()

    individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Redes Neurais Artificiais")

    print("Iniciando treinamento - ANN!")

    geracao = 0
    top1 = None
    fitness = 0

    while ainda_esta_treinando(geracoes, geracao):
        print(f"Geracao {geracao} ###########################")
        top1, resultado_treino = funcao_sem_nome(
            tela, individuos, fitness_medio, fitness_minimo
        )
        fitness = top1.fitness

        ArtificialNeuralNetwork.salva_individuo(melhor_individuo=top1, geracao=geracao)
        individuos = ArtificialNeuralNetwork.mutacao(top1=top1, individuos=individuos)

        if resultado_treino is None:
            print(f"TOP 1 Com fitness insatisfatorio, resetando populacao")
            individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

        geracao += 1

        if (geracoes == -1) and resultado_treino:
            break

    tempo_decorrido = round(time() - inicio, 2)
    top1.tempo_treino = tempo_decorrido
    top1.fitness = fitness

    ArtificialNeuralNetwork.salva_melhor(top1)

    print("Treinamento Finalizado - RNA")


def funcao_sem_nome(tela, individuos, medio, minimo):
    for i in range(len(individuos)):
        jogo = PongGame(tela, LARGURA, ALTURA)
        jogo.treina_ann(individuo_1=individuos[i])

    top1, fitness_medio = ArtificialNeuralNetwork.melhor_individuo(
        individuos=individuos
    )

    if fitness_medio > medio:
        return top1, True

    if top1.fitness < minimo:
        return top1, None

    return top1, False
