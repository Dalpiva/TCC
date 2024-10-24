import pygame
from time import time
import argparse

# Locais
from QLearning import QLearning
from PongGame import PongGame

# Definindo a largura e altura da tela do jogo
LARGURA, ALTURA = 700, 500


def treinar_q_learning(
    episodios: int = 500,
    desconto: float = 0.0001,
    alpha: float = 0.4,
    gamma: float = 0.9,
) -> None:
    """
    Função responsável por treinar um agente utilizando o algoritmo de Q-Learning jogando Pong.

    Args:
        episodios (int, opcional): Número de episódios para o treinamento. Padrão é 500.
        desconto (float, opcional): Epsilon greedy para o Q-Learning. Padrão é 0.0001.
        alpha (float, opcional): Taxa de aprendizado do Q-Learning. Padrão é 0.4.
        gamma (float, opcional): Fator de desconto futuro para o Q-Learning. Padrão é 0.9.
    """
    inicio = time()

    # Configurando a tela para o jogo
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Treinamento Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning(fator_desconto=desconto, alpha=alpha, gamma=gamma)

    for i in range(episodios):
        jogo.bola.spawn_aleatorio((LARGURA, ALTURA))
        agente.acoes = 0
        jogo.treinar_com_qlearning(
            agente=agente
        )  # Usando o novo nome do método para treinamento

        if i % 20 == 0:
            QLearning.salva_agente(episodio=i, agente=agente)

        print(f"Episódio {i+1}, Epsilon: {agente.epsilon}, Recompensa: {agente.acoes}")

    tempo_decorrido = round(time() - inicio, 2)
    agente.tempo_treino = tempo_decorrido

    QLearning.salva_final(agente=agente)

    print("Treinamento Finalizado - QLearning!")
    print(f"Tempo Decorrido: {tempo_decorrido} segundos")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Jogue uma Partida de Pong contra uma IA",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--episodes",
        type=int,
        help="""Número de episódios para treinar o agente
        (padrão em 500)""",
    )

    parser.add_argument(
        "--alpha",
        type=float,
        help="""Taxa de aprendizado
            Valores entre 0 e 1.
            Valores próximos a 1 fazem o agente mais sensitivo a novas informações
            Valores próximos a 0 fazem o agente mais conservador
            (Padrão em 0.9)""",
    )

    parser.add_argument(
        "--gamma",
        type=float,
        help="""Fator de desconto
            Valores de 0 a 1
            Valores próximos a 1 fazem o agente agir se em prol de recompensas a longo prazo
            Valores próximos a 0 fazem o agente focar em recompensas imediatas
            (Padão em 0.4)""",
    )

    parser.add_argument(
        "--discount",
        type=float,
        help="""Fator para ajustar epsilon (exploração versus exploração)
            Determina o quão rápido será o desconto no epsilon greedy
            Epsilon greedy inicia-se em 1
        (Padrão em 0.0001)""",
    )

    args = parser.parse_args()

    if args.episodes is None:
        print("Insira os Episódios")
        exit()

    if args.alpha is None:
        print("Insira o valor Alpha")
        exit()

    if args.gamma is None:
        print("Insira o valor Gamma")
        exit()

    if args.discount is None:
        print("Insira o valor de exploração versus exploração")
        exit()

    treinar_q_learning(args.episodes, args.alpha, args.gamma, args.discount)
