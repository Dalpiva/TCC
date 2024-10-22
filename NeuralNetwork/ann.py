import numpy as np
import pickle
from typing import List, Tuple


class ArtificialNeuralNetwork:
    def __init__(self, neuronios_entrada: int, neuronios_saida: int) -> None:
        """
        Inicializa a Rede Neural Artificial com o número de neurônios de entrada e saída.

        Args:
            neuronios_entrada (int): Número de neurônios na camada de entrada.
            neuronios_saida (int): Número de neurônios na camada de saída.
        """
        self.fitness = 0
        self.estrutura_rede = [neuronios_entrada, neuronios_saida]
        self.nos = self.gera_nos(estrutura_rede=self.estrutura_rede)
        self.pesos = self.gera_pesos(estrutura_rede=self.estrutura_rede)
        self.tempo_treino = 0

    def gera_nos(self, estrutura_rede: List[int]) -> List[np.ndarray]:
        """
        Gera os nós da rede neural com valores aleatórios entre -1 e 1.

        Args:
            estrutura_rede (List[int]): Estrutura da rede com o número de neurônios por camada.

        Retorna:
            List[np.ndarray]: Lista contendo os nós de cada camada.
        """
        nos = []

        for i in range(len(estrutura_rede) - 1):
            nos.append(np.random.rand(estrutura_rede[i + 1]) * 2 - 1)

        return nos

    def gera_pesos(self, estrutura_rede: List[int]) -> List[np.ndarray]:
        """
        Gera os pesos da rede neural com valores aleatórios entre -1 e 1.

        Args:
            estrutura_rede (List[int]): Estrutura da rede com o número de neurônios por camada.

        Retorna:
            List[np.ndarray]: Lista contendo os pesos de cada camada.
        """
        pesos = []

        for i in range(len(estrutura_rede) - 1):
            pesos.append(
                np.random.rand(estrutura_rede[i], estrutura_rede[i + 1]) * 2 - 1
            )

        return pesos

    def muta_nos(self, nos: List[np.ndarray]) -> List[np.ndarray]:
        """
        Realiza mutação nos nós, aplicando uma variação normal.

        Args:
            nos (List[np.ndarray]): Lista de nós a serem mutados.

        Retorna:
            List[np.ndarray]: Lista de novos nós após a mutação.
        """
        novos_nos = nos.copy()

        for i in range(len(novos_nos)):
            for linha in range(len(novos_nos[i])):
                novos_nos[i][linha] = np.random.normal(novos_nos[i][linha], 0.01)
        return novos_nos

    def muta_pesos(self, pesos: List[np.ndarray]) -> List[np.ndarray]:
        """
        Realiza mutação nos pesos, aplicando uma variação normal.

        Args:
            pesos (List[np.ndarray]): Lista de pesos a serem mutados.

        Retorna:
            List[np.ndarray]: Lista de novos pesos após a mutação.
        """
        novos_pesos = pesos.copy()

        for i in range(len(novos_pesos)):
            for linha in range(len(novos_pesos[i])):
                for coluna in range(len(novos_pesos[i][linha])):
                    novos_pesos[i][linha][coluna] = np.random.normal(
                        novos_pesos[i][linha][coluna], 0.01
                    )
        return novos_pesos

    def cria_entrada(self, raquete_y: float, bola_y: float) -> np.ndarray:
        """
        Cria o vetor de entrada para a rede neural.

        Args:
            raquete_y (float): Posição Y da raquete.
            bola_y (float): Posição Y da bola.

        Retorna:
            np.ndarray: Vetor de entrada com as posições da raquete e bola.
        """
        return np.array([[raquete_y, bola_y]])

    def calcula_saida(
        self, input: np.ndarray, nos: List[np.ndarray], pesos: List[np.ndarray]
    ) -> int:
        """
        Calcula a saída da rede neural com base na entrada e nos pesos e nós da rede.

        Args:
            input (np.ndarray): Vetor de entrada para a rede.
            nos (List[np.ndarray]): Lista de nós da rede.
            pesos (List[np.ndarray]): Lista de pesos da rede.

        Retorna:
            int: Índice da saída resultante (0, 1 ou 2).
        """
        camadas = [np.transpose(input)]
        camada_anterior = np.transpose(input)

        estrutura_rede_reduzida = self.estrutura_rede[1:]

        for k in range(len(estrutura_rede_reduzida)):
            camada_atual = np.empty((estrutura_rede_reduzida[k], 1))

            result = np.matmul(np.transpose(pesos[k]), camada_anterior) + np.transpose(
                np.array([nos[k]])
            )
            for i in range(len(camada_atual)):
                # Função de ativação ReLU
                camada_atual[i] = max(0, result[i])

            camadas.append(camada_atual)
            camada_anterior = camada_atual.copy()

        return camadas[-1].tolist().index(max(camadas[-1].tolist()))

    @staticmethod
    def melhor_individuo(
        individuos: List["ArtificialNeuralNetwork"],
    ) -> Tuple["ArtificialNeuralNetwork", float]:
        """
        Encontra o melhor indivíduo da população com base no fitness.

        Args:
            individuos (List[ArtificialNeuralNetwork]): Lista de indivíduos da população.

        Retorna:
            Tuple[ArtificialNeuralNetwork, float]: O melhor indivíduo e o fitness médio da população.
        """
        top1, top2, top3 = (
            ArtificialNeuralNetwork(2, 3),
            ArtificialNeuralNetwork(2, 3),
            ArtificialNeuralNetwork(2, 3),
        )
        fitness_total = 0

        for individuo in individuos:
            fitness_atual = individuo.fitness

            if fitness_atual > top1.fitness:
                top3 = top2
                top2 = top1
                top1 = individuo
            elif fitness_atual > top2.fitness:
                top3 = top2
                top2 = individuo
            elif fitness_atual > top3.fitness:
                top3 = individuo

            fitness_total += fitness_atual

        fitness_medio = fitness_total / len(individuos)

        return top1, fitness_medio

    @staticmethod
    def mutacao(
        top1: "ArtificialNeuralNetwork", individuos: List["ArtificialNeuralNetwork"]
    ) -> List["ArtificialNeuralNetwork"]:
        """
        Aplica mutação nos indivíduos da população com base no melhor indivíduo (top1).

        Args:
            top1 (ArtificialNeuralNetwork): O melhor indivíduo da geração.
            individuos (List[ArtificialNeuralNetwork]): Lista de indivíduos a serem mutados.

        Retorna:
            List[ArtificialNeuralNetwork]: Lista de indivíduos após a mutação.
        """
        for individuo in individuos:
            individuo.nos = top1.muta_nos(nos=top1.nos)
            individuo.pesos = top1.muta_pesos(pesos=top1.pesos)
            individuo.fitness = 0

        return individuos

    def calcula_fitness(self, informacao_jogo) -> None:
        """
        Calcula o fitness do indivíduo com base no número de acertos da raquete esquerda.

        Args:
            informacao_jogo: Objeto contendo as informações do jogo, como o número de acertos da raquete esquerda.
        """
        self.fitness += informacao_jogo.acertos_esq

    @staticmethod
    def gera_populacao(populacao: int) -> List["ArtificialNeuralNetwork"]:
        """
        Gera uma população de indivíduos.

        Args:
            populacao (int): Número de indivíduos a serem gerados.

        Retorna:
            List[ArtificialNeuralNetwork]: Lista de indivíduos gerados.
        """
        return [ArtificialNeuralNetwork(2, 3) for _ in range(populacao)]

    @staticmethod
    def salva_individuo(
        melhor_individuo: "ArtificialNeuralNetwork", geracao: int
    ) -> None:
        """
        Salva o melhor indivíduo de uma geração em um arquivo pickle.

        Args:
            melhor_individuo (ArtificialNeuralNetwork): O melhor indivíduo a ser salvo.
            geracao (int): O número da geração do indivíduo.
        """
        with open(
            f"NeuralNetwork/geracoes/melhor_individuo_geracao_{geracao}.pkl", "wb"
        ) as f:
            pickle.dump(melhor_individuo, f)

    @staticmethod
    def salva_melhor(melhor_individuo: "ArtificialNeuralNetwork") -> None:
        """
        Salva o melhor indivíduo geral em um arquivo pickle.

        Args:
            melhor_individuo (ArtificialNeuralNetwork): O melhor indivíduo a ser salvo.
        """
        with open(f"NeuralNetwork/geracoes/melhor.pkl", "wb") as f:
            pickle.dump(melhor_individuo, f)

    @staticmethod
    def carrega_individuo(geracao: int) -> "ArtificialNeuralNetwork":
        """
        Carrega um indivíduo de uma geração específica.

        Args:
            geracao (int): O número da geração do indivíduo a ser carregado.

        Retorna:
            ArtificialNeuralNetwork: O indivíduo carregado.
        """
        with open(
            f"NeuralNetwork/geracoes/melhor_individuo_geracao_{geracao}.pkl", "rb"
        ) as f:
            return pickle.load(f)

    @staticmethod
    def carrega_melhor() -> "ArtificialNeuralNetwork":
        """
        Carrega o melhor indivíduo geral salvo.

        Retorna:
            ArtificialNeuralNetwork: O melhor indivíduo geral carregado.
        """
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
    print("Pesos:")
    print(pesos)
    print("Mutação nos:")
    print(muta_nos)
    print("Mutação pesos:")
    print(muta_pesos)
