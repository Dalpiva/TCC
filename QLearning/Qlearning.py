import numpy as np
import pickle


class QLearning:
    def __init__(self, fator_desconto: float, alpha: float, gamma: float) -> None:
        """
        Inicializa o agente de Q-Learning com os parâmetros de aprendizado.

        Args:
            fator_desconto (float): Fator de desconto usado no ajuste do epsilon (exploração).
            alpha (float): Taxa de aprendizado para o ajuste da tabela Q.
            gamma (float): Fator de desconto para recompensas futuras no cálculo Q-Learning.
        """
        self.alpha = alpha
        self.gamma = gamma

        self.fator_desconto = fator_desconto
        self.epsilon_min = 0.1
        self.epsilon = 1

        self.tabela_q = {}
        self.recompensa = 0

        self.acoes = 0
        self.tempo_treino = 0

    def epsilon_greedy(self) -> None:
        """
        Ajusta o valor de epsilon usando a estratégia epsilon-greedy.
        """
        self.epsilon = max(self.epsilon_min, self.epsilon * (1 - self.fator_desconto))

    def proxima_acao(self, estado: tuple, treino: bool = False) -> int:
        """
        Seleciona a próxima ação com base no estado atual usando a política epsilon-greedy.

        Args:
            estado (tuple): O estado atual do ambiente (posição da bola em relação à raquete).
            treino (bool, opcional): Se for True, executa a exploração. Caso contrário, executa a melhor ação. Padrão é False.

        Retorna:
            int: A ação selecionada (0, 1 ou 2).
        """
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

    def atualiza_tabela_q(
        self, estado: tuple, acao: int, recompensa: float, proximo_estado: tuple
    ) -> None:
        """
        Atualiza a tabela Q usando a fórmula do Q-Learning.

        Args:
            estado (tuple): O estado atual do ambiente.
            acao (int): A ação executada no estado atual.
            recompensa (float): A recompensa obtida pela ação.
            proximo_estado (tuple): O próximo estado resultante da ação.
        """
        if proximo_estado not in self.tabela_q:
            self.tabela_q[proximo_estado] = np.zeros(3)

        alvo = recompensa + self.gamma * np.max(self.tabela_q[proximo_estado])
        erro = alvo - self.tabela_q[estado][acao]
        self.tabela_q[estado][acao] += self.alpha * erro

        self.acoes += 1  # Conta o número de ações realizadas

    def recebe_recompensa(self, y_raquete: float, y_bola: float) -> float:
        """
        Calcula a recompensa com base na distância entre a raquete e a bola.

        Args:
            y_raquete (float): Posição Y da raquete.
            y_bola (float): Posição Y da bola.

        Retorna:
            float: O valor da recompensa calculada.
        """
        altura_tela = 500

        recompensa_max = 30  # Metade do tamanho da raquete
        recompensa_min = -30

        centro_y_raquete = y_raquete + 50
        distancia_y = abs(centro_y_raquete - y_bola)

        recompensa = -(distancia_y / altura_tela) * recompensa_max

        RAIO_BOLA = 8
        if distancia_y <= RAIO_BOLA * 2:
            recompensa += 100

        return max(recompensa_min, recompensa)

    def define_estado(self, y_raquete: float, y_bola: float) -> int:
        """
        Define o estado da bola em relação à raquete.

        Args:
            y_raquete (float): Posição Y da raquete.
            y_bola (float): Posição Y da bola.

        Retorna:
            int: O estado da bola em relação à raquete (0 = na linha da raquete, 1 = abaixo, 2 = acima).
        """
        cima_raquete = y_raquete
        baixo_raquete = cima_raquete + 100

        if cima_raquete <= y_bola <= baixo_raquete:
            estado_bola = 0  # A bola está na linha da raquete
        elif y_bola > baixo_raquete:
            estado_bola = 1  # A bola está abaixo da raquete
        else:
            estado_bola = 2  # A bola está acima da raquete

        return estado_bola

    @staticmethod
    def salva_agente(episodio: int, agente: "QLearning") -> None:
        """
        Salva o estado atual do agente (tabela Q) em um arquivo pickle.

        Args:
            episodio (int): O número do episódio atual do treinamento.
            agente (QLearning): O agente a ser salvo.
        """
        with open(f"QLearning/episodios/tabela_q_ep_{episodio}.pkl", "wb") as file:
            pickle.dump(agente, file)

    @staticmethod
    def salva_final(agente: "QLearning") -> None:
        """
        Salva o agente final após o treinamento em um arquivo pickle.

        Args:
            agente (QLearning): O agente a ser salvo.
        """
        with open(f"QLearning/episodios/agente_final.pkl", "wb") as file:
            pickle.dump(agente, file)

    @staticmethod
    def carrega_melhor() -> "QLearning":
        """
        Carrega o melhor agente salvo em um arquivo pickle.

        Retorna:
            QLearning: O agente carregado.
        """
        with open("QLearning/episodios/agente_final.pkl", "rb") as file:
            return pickle.load(file)


if __name__ == "__main__":
    # Exemplo de uso do Q-Learning
    agente = QLearning(fator_desconto=0.01, alpha=0.4, gamma=0.9)
    agente.carrega_melhor()
    print(
        "Valor máximo da tabela Q no estado (0, 0): ",
        np.max(agente.tabela_q.get((0, 0), [0])),
    )
    agente.atualiza_tabela_q((0, 0), 0, 50, (1, 1))
    print(agente.tabela_q)
    print(
        "Novo valor máximo da tabela Q no estado (0, 0): ",
        np.max(agente.tabela_q.get((0, 0), [0])),
    )
