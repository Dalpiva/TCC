import numpy as np
import pickle


class ArtificialNeuralNetwork:

    def __init__(self, neuronios_entrada, neuronios_saida):
        self.fitness = 0
        self.estrutura_rede = [neuronios_entrada, neuronios_saida]
        self.nos = self.gera_nos(estrutura_rede=self.estrutura_rede)
        self.pesos = self.gera_pesos(estrutura_rede=self.estrutura_rede)
        self.tempo_treino = 0

    def gera_nos(self, estrutura_rede):
        nos = []

        for i in range(len(estrutura_rede) - 1):
            nos.append(np.random.rand(estrutura_rede[i + 1]) * 2 - 1)

        return nos

    def gera_pesos(self, estrutura_rede):
        pesos = []

        for i in range(len(estrutura_rede) - 1):
            pesos.append(
                np.random.rand(estrutura_rede[i], estrutura_rede[i + 1]) * 2 - 1
            )

        return pesos

    def muta_nos(self, nos):
        novos_nos = nos.copy()

        for i in range(len(novos_nos)):
            for linha in range(len(novos_nos[i])):
                novos_nos[i][linha] = np.random.normal(novos_nos[i][linha], 0.01)
        return novos_nos

    def muta_pesos(self, pesos):
        novos_pesos = pesos.copy()

        for i in range(len(novos_pesos)):
            for linha in range(len(novos_pesos[i])):
                for coluna in range(len(novos_pesos[i][linha])):
                    novos_pesos[i][linha][coluna] = np.random.normal(
                        novos_pesos[i][linha][coluna], 0.01
                    )
        return novos_pesos

    def cria_entrada(self, raquete_y, bola_y):
        return np.array([[raquete_y, bola_y]])

    def calcula_saida(self, input, nos, pesos):
        camadas = [np.transpose(input)]
        camada_anterior = np.transpose(input)

        estrutura_rede_reduzida = self.estrutura_rede[1:]

        for k in range(len(estrutura_rede_reduzida)):
            camada_atual = np.empty((estrutura_rede_reduzida[k], 1))

            result = np.matmul(np.transpose(pesos[k]), camada_anterior) + np.transpose(
                np.array([nos[k]])
            )
            for i in range(len(camada_atual)):
                # ReLU
                camada_atual[i] = max(0, result[i])

                # Sigmoid
                # camada_atual[i] = 1 / (1 + np.exp(-camada_atual[i]))

            camadas.append(camada_atual)
            camada_anterior = camada_atual.copy()

        return camadas[-1].tolist().index(max(camadas[-1].tolist()))

    def melhor_individuo(individuos):
        top1 = ArtificialNeuralNetwork(2, 3)
        top2 = ArtificialNeuralNetwork(2, 3)
        top3 = ArtificialNeuralNetwork(2, 3)
        fitness_total = 0

        for i in range(len(individuos)):
            fitness_atual = individuos[i].fitness

            if fitness_atual > top1.fitness:
                top3 = top2
                top2 = top1
                top1 = individuos[i]
            elif fitness_atual > top2.fitness:
                top3 = top2
                top2 = individuos[i]
            elif fitness_atual > top3.fitness:
                top3 = individuos[i]

            fitness_total += individuos[i].fitness

        fitness_medio = fitness_total / len(individuos)

        return top1, fitness_medio

    def mutacao(top1, individuos):
        total_individuos = len(individuos)

        for i in range(total_individuos):
            individuos[i].nos = top1.muta_nos(nos=top1.nos)
            individuos[i].pesos = top1.muta_pesos(pesos=top1.pesos)
            individuos[i].fitness = 0

        return individuos

    def calcula_fitness(self, informacao_jogo):
        self.fitness += informacao_jogo.acertos_esq

    def gera_populacao(populacao):
        individuos = []
        for i in range(populacao):
            individuos.append(ArtificialNeuralNetwork(2, 3))

        return individuos

    def salva_individuo(melhor_individuo, geracao):
        with open(
            f"NeuralNetwork/geracoes/melhor_individuo_geracao_{geracao}.pickle", "wb"
        ) as f:
            pickle.dump(melhor_individuo, f)

    def salva_melhor(melhor_individuo):
        with open(f"NeuralNetwork/geracoes/melhor.pkl", "wb") as f:
            pickle.dump(melhor_individuo, f)

    def carrega_individuo(geracao):
        with open(
            f"NeuralNetwork/geracoes/melhor_individuo_geracao_{geracao}.pickle", "rb"
        ) as f:
            return pickle.load(f)

    def carrega_melhor():
        with open("NeuralNetwork/geracoes/melhor.pkl", "rb") as f:
            return pickle.load(f)


if __name__ == "__main__":
    individuo = ArtificialNeuralNetwork(2, 3)
    nos = individuo.nos
    pesos = individuo.pesos
    muta_nos = individuo.muta_nos(nos=nos)
    muta_pesos = individuo.muta_pesos(pesos=pesos)

    print(individuo.estrutura_rede)
    print("Coeficientes:")
    print(nos)
    print("pesos")
    print(pesos)
    print("Mutacao nos")
    print(muta_nos)
    print("Mutacao pesos")
    print(muta_pesos)
