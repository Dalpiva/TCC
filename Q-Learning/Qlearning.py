import numpy as np


# Tudo o que a raquete pode andar no eixo Y
COLUNAS_AMBIENTE = 404
LINHAS_AMBIENTE = 1
ACOES = 3

valores_q = np.zeros((LINHAS_AMBIENTE, COLUNAS_AMBIENTE), ACOES)

# 0 = parar, 1 = cima, baixo = 2
lista_acoes = ["parar", "cima", "baixo"]

recompensas = np.full((LINHAS_AMBIENTE, COLUNAS_AMBIENTE), -1)
