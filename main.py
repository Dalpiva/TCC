# Referencia

# https://github.com/techwithtim/Pong-Python
# https://github.com/techwithtim/NEAT-Pong-Python

from PONG import Jogo
from NeuralNetwork import ArtificialNeuralNetwork
from QLearning import QLearning

import pygame

LARGURA, ALTURA = 700, 500


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

    def treina_ann(self, individuo_1):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.jogada_adversario_perfeito()

            entrada_1 = individuo_1.cria_entrada(
                raquete_y=self.raquete_esquerda.y,
                bola_y=self.bola.y,
                # distancia_bola=abs(self.raquete_esquerda.x - self.bola.x),
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

            informacao_jogo = self.jogo.loop(treino_qlearning=True)
            self.jogo.cria_tela(False, True)
            pygame.display.update()

            # Se alguem errar, para o jogo
            if (
                informacao_jogo.pontuacao_dir >= 1
                or informacao_jogo.pontuacao_esq >= 1
                or informacao_jogo.acertos_esq > 50
            ):
                individuo_1.calcula_fitness(
                    informacao_jogo=informacao_jogo,
                )
                run = False

    def jogar_ann(self, individuo):
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
            if teclas[pygame.K_UP]:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            elif teclas[pygame.K_DOWN]:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            entrada = individuo.cria_entrada(
                raquete_y=self.raquete_esquerda.y,
                bola_y=self.bola.y,
                # distancia_bola=abs(self.raquete_esquerda.x - self.bola.x),
            )

            decisao = individuo.calcula_saida(
                input=entrada, nos=individuo.nos, pesos=individuo.pesos
            )

            if decisao == 0:
                pass
            elif decisao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            else:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()

    def treina_qlearning(self, agente):
        run = True
        acao = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.jogada_adversario_perfeito()

            # -----
            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)
            estado = (estado_bola, acao)

            acao = agente.proxima_acao(estado=estado, treino=True)

            if acao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            elif acao == 2:
                self.jogo.move_raquetes(esquerda=True, cima=False)

            # Treinamento
            recompensa = agente.recebe_recompensa(self.raquete_esquerda.y, self.bola.y)
            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)

            proximo_estado = (estado_bola, acao)
            agente.atualiza_tabela_q(estado, acao, recompensa, proximo_estado)
            agente.recompensa += recompensa
            # -----

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

            if self.jogo.pontuacao_dir == 5 or self.jogo.pontuacao_esq == 5:
                self.jogo.reset()
                run = False

            if self.jogo.acertos_dir > 50:
                self.jogo.reset()
                run = False

    def jogar_qlearning(self, agente):
        run = True
        acao = 0
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_UP]:
                self.jogo.move_raquetes(esquerda=False, cima=True)
            elif teclas[pygame.K_DOWN]:
                self.jogo.move_raquetes(esquerda=False, cima=False)

            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)
            estado = (estado_bola, acao)

            acao = agente.proxima_acao(estado=estado)

            if acao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=True)
            elif acao == 2:
                self.jogo.move_raquetes(esquerda=True, cima=False)
            # -----

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

            """if self.jogo.pontuacao_dir == 5 or self.jogo.pontuacao_esq == 5:
                self.jogo.reset()
                run = False

            if self.jogo.acertos_dir > 50:
                self.jogo.reset()
                run = False"""

        pygame.quit()


def jogar():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Player x Oponente Perfeito")

    jogo = PongGame(tela, LARGURA, ALTURA)
    jogo.jogar()


def treinamento_ann(populacao=100):
    individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Redes Neurais Artificiais")

    print("Iniciando treinamento - ANN!")

    geracao = 0

    while True:
        print(f"Geracao {geracao} ###########################")
        top1, resultado_treino = funcao_sem_nome(tela=tela, individuos=individuos)

        ArtificialNeuralNetwork.salva_individuo(melhor_individuo=top1, geracao=geracao)
        individuos = ArtificialNeuralNetwork.mutacao(top1=top1, individuos=individuos)

        if resultado_treino is None:
            print(f"TOP 1 Com fitness insatisfatorio, resetando populacao")
            individuos = ArtificialNeuralNetwork.gera_populacao(populacao=populacao)

        geracao += 1

        if resultado_treino:
            break

    print("Treinamento Finalizado!")


def funcao_sem_nome(tela, individuos):
    for i in range(len(individuos)):
        jogo = PongGame(tela, LARGURA, ALTURA)
        jogo.treina_ann(individuo_1=individuos[i])

    top1, fitness_medio = ArtificialNeuralNetwork.melhor_individuo(
        individuos=individuos
    )

    if fitness_medio > 15:
        return top1, True

    if top1.fitness < 5:
        return top1, None

    return top1, False


def jogar_ann(geracao):
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Redes Neurais Artificiais")

    jogo = PongGame(tela, LARGURA, ALTURA)

    vencedor = ArtificialNeuralNetwork.carrega_individuo(geracao=geracao)

    jogo.jogar_ann(individuo=vencedor)


def treinamento_q_learning():
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Treinamento Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning()

    for i in range(501):
        jogo.treina_qlearning(agente=agente)

        if i % 10 == 0:
            agente.salva_tabela(episodio=i + 1)

        print(
            f"Episodio {i+1}, Epsilon: {agente.epsilon}, recompensa: {agente.recompensa}"
        )


def jogar_q_learning(episodio=251):
    LARGURA, ALTURA = 700, 500
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("PONG - TCC WESLEY - Jogo Q-Learning")

    jogo = PongGame(tela, LARGURA, ALTURA)
    agente = QLearning()

    # Bom EP em 251
    agente.carrega_tabela(arq=f"QLearning/episodios/tabela_q_ep_{episodio}.pkl")

    jogo.jogar_qlearning(agente=agente)


if __name__ == "__main__":
    # jogar()
    treinamento_ann()
    # jogar_ann(geracao=12)
    # treinamento_q_learning()
    # jogar_q_learning(episodio=251)
