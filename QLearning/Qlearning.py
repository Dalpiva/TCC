import numpy as np
import pickle


class QLearning:
    def __init__(self, fator_desconto=0.00001, epsilon_min=0.1, epsilon=1):
        self.alpha = 0.4
        self.gamma = 0.7

        self.fator_desconto = fator_desconto
        self.epsilon_min = epsilon_min
        self.epsilon = epsilon

        self.tabela_q = {}
        self.recompensas = []
        self.episodios = []
        self.media = []

        self.recopensa = 0

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

    def salva_tabela(self, episodio):
        with open(f"tabela_q_ep_{episodio}.pkl", "wb") as file:
            pickle.dump(self.tabela_q, file)

    def carrega_tabela(self):
        with open("", "rb") as file:
            self.tabela_q = pickle.load(file)

    def recebe_recompensa(self, y_raquete, y_bola):
        altura_tela = 500

        recompensa_max = 50  # metade do tamanho da raquete, o centro
        recompensa_min = -50

        centro_y_raquete = y_raquete + 50
        distancia_y = abs(centro_y_raquete - y_bola)

        recompensa = -(distancia_y / altura_tela) * recompensa_max

        if distancia_y < recompensa_max:
            recompensa += recompensa_max

        return max(recompensa_min, recompensa)

    def define_estado(self, y_raquete, y_bola):
        fundo_raquete = y_raquete
        topo_raquete = fundo_raquete - 100

        if topo_raquete <= y_bola <= fundo_raquete:
            estado_bola = 0  # a bola esta na linha da raquete
        elif y_bola > fundo_raquete:
            estado_bola = 1  # a bola esta abaixo da raquete
        else:
            estado_bola = 2  # a bola esta acima da raquete

        return estado_bola


if __name__ == "__main__":
    qlearning = QLearning()
    qlearning.epsilon_greedy()
    print(qlearning.epsilon)
