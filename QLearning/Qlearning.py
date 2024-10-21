import numpy as np
import pickle
import csv


class QLearning:
    def __init__(self, fator_desconto, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma

        self.fator_desconto = fator_desconto
        self.epsilon_min = 0.1
        self.epsilon = 1

        self.tabela_q = {}
        self.recompensa = 0

        self.acoes = 0
        self.tempo_treino = 0

    def epsilon_greedy(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * (1 - self.fator_desconto))

    def proxima_acao(self, estado, treino=False):
        if estado not in self.tabela_q:
            self.tabela_q[estado] = np.zeros(3)

        if treino:
            self.epsilon_greedy()

            if np.random.uniform() < self.epsilon:
                acao = np.random.choice(3)
            else:
                acao = np.argmax(self.tabela_q[estado])
        else:
            acao = np.argmax(self.tabela_q[estado])

        return acao

    def atualiza_tabela_q(self, estado, acao, recompensa, proximo_estado):
        if proximo_estado not in self.tabela_q:
            self.tabela_q[proximo_estado] = np.zeros(3)

        alvo = recompensa + self.gamma * np.max(self.tabela_q[proximo_estado])
        erro = alvo - self.tabela_q[estado][acao]
        self.tabela_q[estado][acao] += self.alpha * erro

        # conta quantas acoes
        self.acoes += 1

    def recebe_recompensa(self, y_raquete, y_bola):
        altura_tela = 500

        recompensa_max = 30  # metade do tamanho da raquete, o centro
        recompensa_min = -30

        centro_y_raquete = y_raquete + 50
        distancia_y = abs(centro_y_raquete - y_bola)

        recompensa = -(distancia_y / altura_tela) * recompensa_max

        RAIO_BOLA = 8
        if distancia_y <= RAIO_BOLA * 2:
            recompensa += 100

        return max(recompensa_min, recompensa)

    def define_estado(self, y_raquete, y_bola):
        cima_raquete = y_raquete
        baixo_raquete = cima_raquete + 100

        if cima_raquete <= y_bola <= baixo_raquete:
            estado_bola = 0  # a bola esta na linha da raquete
        elif y_bola > baixo_raquete:
            estado_bola = 1  # a bola esta abaixo da raquete
        else:
            estado_bola = 2  # a bola esta acima da raquete

        return estado_bola

    def salva_agente(episodio, agente):
        with open(f"QLearning/episodios/tabela_q_ep_{episodio}.pkl", "wb") as file:
            pickle.dump(agente, file)

    def salva_final(agente):
        with open(f"QLearning/episodios/agente_final.pkl", "wb") as file:
            pickle.dump(agente, file)

    def carrega_melhor():
        with open("QLearning/episodios/agente_final.pkl", "rb") as file:
            return pickle.load(file)


if __name__ == "__main__":
    agente = QLearning()
    agente.carrega_tabela(arq=f"QLearning/episodios/tabela_q_ep_{491}.pkl")
    print("NOVO VALOR: ", np.max(agente.tabela_q[(0, 0)]))
    agente.atualiza_tabela_q((0, 0), 0, 50, (1, 1))
    print(agente.tabela_q)
    print("NOVO VALOR: ", np.max(agente.tabela_q[(0, 0)]))
