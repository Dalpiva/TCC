import numpy as np


class ArtificialNeuralNetwork:
    # 3 neuronios de entrada, 3 de saida, sem camada escondida
    estrutura_rede = [3, 3]

    def __init__(self):
        self.fitness = 0
        self.coeficiente = self.gera_coeficentes(estrutura_rede=self.estrutura_rede)
        self.peso = self.gera_pesos(estrutura_rede=self.estrutura_rede)

    def gera_coeficentes(self, estrutura_rede):
        coeficientes = []

        for i in range(len(estrutura_rede) - 1):
            coeficientes.append(
                np.random.rand(estrutura_rede[i], estrutura_rede[i + 1]) * 2 - 1
            )

        return coeficientes

    def gera_pesos(self, estrutura_rede):
        pesos = []

        for i in range(len(estrutura_rede) - 1):
            pesos.append(np.random.rand(estrutura_rede[i + 1]) * 2 - 1)

        return pesos

    def muta_coeficentes(self, coeficientes):
        novos_coeficientes = coeficientes.copy()

        for i in range(len(novos_coeficientes)):
            for linha in range(len(novos_coeficientes[i])):
                for coluna in range(len(novos_coeficientes[i][linha])):
                    novos_coeficientes[i][linha][coluna] = np.random.normal(
                        novos_coeficientes[i][linha][coluna], 1
                    )
        return novos_coeficientes

    def muta_pesos(self, pesos):
        novas_pesos = pesos.copy()

        for i in range(len(novas_pesos)):
            for linha in range(len(novas_pesos[i])):
                novas_pesos[i][linha] = np.random.normal(novas_pesos[i][linha], 1)
        return novas_pesos

    def cria_entrada(self, raquete_y, bola_y, distancia_bola):
        return np.array([[raquete_y, bola_y, distancia_bola]])

    def calcula_saida(self, input, coefs, pesos):
        camadas = [np.transpose(input)]
        camada_anterior = np.transpose(input)

        estrutura_rede_atualizada = self.estrutura_rede[1:]

        for k in range(len(estrutura_rede_atualizada)):
            camada_atual = np.empty((estrutura_rede_atualizada[k], 1))

            result = np.matmul(np.transpose(coefs[k]), camada_anterior) + np.transpose(
                np.array([pesos[k]])
            )
            for i in range(len(camada_atual)):
                # RELu
                camada_atual[i] = max(0, result[i])

                # Sigmoid
                # camada_atual[i] = 1 / (1 + np.exp(-camada_atual[i]))

            camadas.append(camada_atual)
            camada_anterior = camada_atual.copy()

        return camadas[-1].tolist().index(max(camadas[-1].tolist()))

    def melhores_individuos(individuos):
        top1 = ArtificialNeuralNetwork()
        top2 = ArtificialNeuralNetwork()
        top3 = ArtificialNeuralNetwork()

        for i in range(len(individuos)):
            fitness_atual = individuos[i].fitness

            if fitness_atual > top1.fitness:
                top3 = top2  # Desloca o antigo segundo melhor para terceiro melhor
                top2 = top1  # Desloca o antigo melhor para segundo melhor
                top1 = individuos[i]  # Atualiza o melhor fitness
            # Verifica se deve ser inserido na segunda posição
            elif fitness_atual > top2.fitness:
                top3 = top2  # Desloca o antigo segundo melhor para terceiro melhor
                top2 = individuos[i]  # Atualiza o segundo melhor fitness
            # Verifica se deve ser inserido na terceira posição
            elif fitness_atual > top3.fitness:
                top3 = individuos[i]  # Atualiza o terceiro melhor fitness

        print("Fitness - TOP 1: ", top1.fitness)
        print("Fitness - TOP 2: ", top2.fitness)
        print("Fitness - TOP 3: ", top3.fitness)
        print("")

        return top1, top2, top3

    def mutacao(
        top1,
        top2,
        top3,
        individuos,
    ):
        total_individuos = len(individuos)
        perc_t2 = int(total_individuos * 0.2)
        perc_t3 = int(total_individuos * 0.1)

        for i in range(total_individuos):
            if i < perc_t3:
                individuos[i].coeficiente = top3.muta_coeficentes(
                    coeficientes=top3.coeficiente
                )
                individuos[i].peso = top3.muta_pesos(pesos=top3.peso)
                individuos[i].fitness = 0
            elif i < perc_t2:
                individuos[i].coeficiente = top2.muta_coeficentes(
                    coeficientes=top2.coeficiente
                )
                individuos[i].peso = top2.muta_pesos(pesos=top2.peso)
                individuos[i].fitness = 0
            else:
                individuos[i].coeficiente = top1.muta_coeficentes(
                    coeficientes=top1.coeficiente
                )
                individuos[i].peso = top1.muta_pesos(pesos=top1.peso)
                individuos[i].fitness = 0

        return individuos


if __name__ == "__main__":
    individuo = ArtificialNeuralNetwork()
    coef = individuo.coeficiente
    pesos = individuo.peso
    muta_coef = individuo.muta_coeficentes(coeficientes=coef)
    muta_con = individuo.muta_pesos(pesos=pesos)

    print("Coeficientes:")
    print(coef)
    print("pesos")
    print(pesos)
    print("Mutacao coef")
    print(muta_coef)
    print("Mutacao conn")
    print(muta_con)
