import pygame
from time import time
from NeuralNetwork import ArtificialNeuralNetwork
from PongGame import PongGame

# Definindo a largura e altura da tela do jogo
LARGURA, ALTURA = 700, 500


def esta_treinando(geracoes_totais: int, geracao_atual: int) -> bool:
    """
    Verifica se o processo de treinamento da rede neural ainda deve continuar.

    Args:
        geracoes_totais (int): O número total de gerações desejado para o treinamento.
        geracao_atual (int): O número da geração atual.

    Retorna:
        bool: Retorna True se o treinamento ainda deve continuar, caso contrário False.
    """
    if geracoes_totais == -1:
        return True
    return geracao_atual < geracoes_totais


def treinar_rede_neural_artificial(
    populacao: int = 100,
    geracoes: int = -1,
    fitness_medio: int = 15,
    fitness_minimo: int = 5,
) -> None:
    """
    Função responsável por treinar uma população de indivíduos usando Redes Neurais Artificiais jogando Pong.

    Args:
        populacao (int, opcional): O número de indivíduos na população inicial. Padrão é 100.
        geracoes (int, opcional): O número total de gerações para treinar. -1 significa treinamento até atingir o critério. Padrão é -1.
        fitness_medio (int, opcional): O valor médio de fitness desejado para finalizar o treinamento. Padrão é 15.
        fitness_minimo (int, opcional): O valor mínimo de fitness aceito para um indivíduo. Padrão é 5.
    """
    inicio = time()

    # Gera a população inicial de indivíduos
    individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Redes Neurais Artificiais")

    print("Iniciando treinamento - ANN!")

    geracao = 0
    top1 = None
    fitness = 0

    # Loop principal de treinamento
    while esta_treinando(geracoes, geracao):
        print(f"Geração {geracao} ###########################")

        # Avaliação dos indivíduos e obtenção do melhor
        top1, resultado_treino = avaliar_individuos(
            tela, individuos, fitness_medio, fitness_minimo
        )
        fitness = top1.fitness

        ArtificialNeuralNetwork.salva_individuo(melhor_individuo=top1, geracao=geracao)
        individuos = ArtificialNeuralNetwork.mutacao(top1=top1, individuos=individuos)

        if resultado_treino is None:
            # print("TOP 1 com fitness insatisfatório, resetando população.")
            individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

        geracao += 1

        # Se for um treinamento contínuo (-1), finalize ao atingir um bom resultado
        if (geracoes == -1) and resultado_treino:
            break

    # Finalização do treinamento
    tempo_decorrido = round(time() - inicio, 2)
    top1.tempo_treino = tempo_decorrido
    top1.fitness = fitness

    ArtificialNeuralNetwork.salva_melhor(top1)

    print("Treinamento Finalizado - RNA")
    print(f"Tempo decorrido: {tempo_decorrido} segundos")


def avaliar_individuos(
    tela: pygame.Surface,
    individuos: list,
    fitness_medio_desejado: int,
    fitness_minimo: int,
):
    """
    Avalia todos os indivíduos em uma geração e retorna o melhor indivíduo junto com o resultado do treino.

    Args:
        tela (pygame.Surface): Superfície onde o jogo será renderizado.
        individuos (list): Lista de indivíduos a serem avaliados.
        fitness_medio_desejado (int): Valor desejado de fitness médio para continuar o treinamento.
        fitness_minimo (int): Valor mínimo de fitness para determinar se a população é satisfatória.

    Retorna:
        tuple: O melhor indivíduo e um valor booleano ou None, indicando o estado do treinamento.
    """
    for i in range(len(individuos)):
        jogo = PongGame(tela, LARGURA, ALTURA)
        jogo.treinar_ann(individuo_1=individuos[i])

    top1, fitness_medio_atual = ArtificialNeuralNetwork.melhor_individuo(
        individuos=individuos
    )

    if fitness_medio_atual > fitness_medio_desejado:
        return top1, True

    if top1.fitness < fitness_minimo:
        return top1, None

    return top1, False
