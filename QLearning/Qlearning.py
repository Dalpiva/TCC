import numpy as np


class QLearning:
    # Tudo o que a raquete pode andar no eixo Y
    COLUNAS_AMBIENTE = 404
    LINHAS_AMBIENTE = 493
    ACOES = 3

    valores_q = np.zeros((LINHAS_AMBIENTE, COLUNAS_AMBIENTE, ACOES))

    # 0 = parar, 1 = cima, baixo = 2
    lista_acoes = ["parar", "cima", "baixo"]

    recompensas = np.full((LINHAS_AMBIENTE, COLUNAS_AMBIENTE), -1)
    for i in range(min(COLUNAS_AMBIENTE, LINHAS_AMBIENTE)):
        recompensas[i, i] = 100

    for i in range(LINHAS_AMBIENTE):
        for j in range(COLUNAS_AMBIENTE):
            if i != j:  # Para não alterar a diagonal principal já definida
                distancia = abs(i - j)
                nivel_penalidade = 1 + (distancia // 50)
                recompensas[i, j] = -nivel_penalidade

    def procura_bola(self, linha_atual, coluna_atual):
        if linha_atual > self.LINHAS_AMBIENTE - 1:
            linha_atual = self.LINHAS_AMBIENTE - 1
        if coluna_atual > self.COLUNAS_AMBIENTE - 1:
            coluna_atual = self.COLUNAS_AMBIENTE - 1

        if self.recompensas[linha_atual][coluna_atual] == 100:
            return True
        else:
            return False

    # Epsilon greedy
    def proxima_acao(self, linha_atual, coluna_atual, epsilon):
        if linha_atual > self.LINHAS_AMBIENTE - 1:
            linha_atual = self.LINHAS_AMBIENTE - 1
        if coluna_atual > self.COLUNAS_AMBIENTE - 1:
            coluna_atual = self.COLUNAS_AMBIENTE - 1

        if np.random.random() < epsilon:
            acao = np.argmax(self.valores_q[linha_atual])
            # if acao > 1:
            # print(self.valores_q[linha_atual])

            if acao > 2:
                acao = 2
            return acao
        else:
            # Escolhe uma acao aleatoriamente entre as tres possiveis
            return np.random.randint(self.ACOES)

    def proxima_posicao(self, coluna_atual, acao):
        if coluna_atual > self.COLUNAS_AMBIENTE - 1:
            coluna_atual = self.COLUNAS_AMBIENTE - 1

        decisao = 0

        if self.lista_acoes[acao] == "parar" and coluna_atual > 0:
            decisao = 0
        elif (
            self.lista_acoes[acao] == "cima"
            and coluna_atual < self.COLUNAS_AMBIENTE - 1
        ):
            decisao = 1
        elif self.lista_acoes[acao] == "baixo" and coluna_atual > self.COLUNAS_AMBIENTE:
            decisao = 2

        return decisao


"""def get_acao(localizacao_atual):
    localizacao_atual"""


"""def treinamento(episodios, posicao_atual):
    epsilon = 0.9
    fator_disconto = 0.9
    taxa_aprendizado = 0.9

    for episode in range(episodios):
        if not procura_bola(posicao_atual):
            acao = proxima_acao(index_coluna_atual=posicao_atual, epsilon=epsilon)

            index, decisao = proxima_posicao(
                index_acao=acao, index_coluna_atual=posicao_atual
            )

            recompensa = recompensas[index]"""


if __name__ == "__main__":
    qlearning = QLearning()
    print(qlearning.recompensas)
