# Pong AI - Trabalho de Conclusão de Curso
Este projeto é uma implementação clássica do jogo Pong em Python, com componentes de IA adicionais para treinar agentes usando Q-Learning e Redes Neurais Artificiais (RNA). O projeto foi desenvolvido como parte do meu TCC (Trabalho de Conclusão de Curso).

### Tabela de Conteúdos

- [Visão Geral](https://github.com/Dalpiva/TCC?tab=readme-ov-file#vis%C3%A3o-geral)
- [Funcionalidades](https://github.com/Dalpiva/TCC?tab=readme-ov-file#funcionalidades)
- [Instalação](https://github.com/Dalpiva/TCC?tab=readme-ov-file#instala%C3%A7%C3%A3o)
- [Como Executar](https://github.com/Dalpiva/TCC?tab=readme-ov-file#como-executar)
    - Modo Padrão
    - Modo IA (RNA)
    - Modo Q-Learning
- [Treinamento de IA](https://github.com/Dalpiva/TCC?tab=readme-ov-file#treinamento-de-ia)
    - Treinamento com Q-Learning
    - Treinamento com Redes Neurais Artificiais
- [Estrutura do Projeto](https://github.com/Dalpiva/TCC?tab=readme-ov-file#estrutura-do-projeto)
- [Dependências](https://github.com/Dalpiva/TCC?tab=readme-ov-file#depend%C3%AAncias)

## Visão geral

Este projeto estende o jogo clássico Pong com capacidades de IA, proporcionando uma plataforma para experimentos com aprendizado por reforço e redes neurais. Os agentes de IA aprendem a jogar Pong, treinando-se por meio de Q-Learning ou Redes Neurais Artificiais (RNA).

### Funcionalidades 
- Jogo Pong Clássico: Jogador contra oponente perfeito ou IA contra IA.
- IA Q-Learning: Treine um agente de IA para jogar Pong usando Q-Learning.
- IA Redes Neurais: Treine e jogue contra uma IA controlada por uma Rede Neural Artificial.
- Feedback Visual: Assista aos agentes de IA enquanto treinam e competem.
- Jogabilidade Configurável: Personalize parâmetros como dificuldade, episódios de treinamento e muito mais.

## Instalação
1 - Clone o repositório:
```bash
git clone https://github.com/Dalpiva/TCC.git
cd pong-ia
```
2 - Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv .venv
source .venv/bin/activate # No windows: .venv\Scripts\activate
```
3 - Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar
### Modo Padrão
Para executar o Pong clássico (Jogador contra IA):
python main.py --mode 
```bash
python main.py --mode standard
```

### Modo IA (RNA)
Para executar o jogo com uma IA de Rede Neural pré-treinada:
```bash
python main.py --mode ann
```

### Modo Q-Learning
Para executar o jogo com um agente de Q-Learning pré-treinado:
```bash
python main.py --mode qlearning
```

## Treinamento de IA
### Treinamento com Redes Neurais Artificiais
Para treinar um agente de IA usando Redes Neurais (RNA):

```bash
python train_ann.py --population 100 --generations 50 --fitness-min 5 --fitness-avg 15
```
- `--population` : O tamanho da população de RNAs.
- `--generations`: Número de gerações para o treinamento.
- `--fitness-min`: Fitness mínimo necessário para um indivíduo avançar.
- `--fitness-avg`: Fitness médio para continuar o processo de treinamento.

### Treinamento com Q-Learning
Você pode treinar o agente de Q-Learning executando:
```bash
python train_qlearning.py --episodes 500 --alpha 0.4 --gamma 0.9 --discount 0.0001
```

- `--episodes`: Número de episódios para treinar o agente.
- `--alpha`: Taxa de aprendizado.
- `--gamma`: Fator de desconto.
- `--discount`: Fator para ajustar epsilon (exploração versus exploração).

## Estrutura do Projeto
├── NeuralNetwork/&emsp;&emsp; # Diretório relacionado as Redes Neurais Artificiais<br/>
│   ├── geracoes/&emsp;&emsp;&emsp;&emsp;# Diretório para salvar gerações de RNA <br/>
│   ├── __init__.py<br/>
│   └── ann.py&emsp;&emsp;&emsp;&emsp; &emsp; # Lógica dos individuos da RNA <br /> 
├── PONG/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; # Diretório das Classes do jogo<br/>
│   ├── __init__.py<br/>
│   ├── bola.py &emsp; &emsp; &emsp; &emsp; # Classe Bola <br/>
│   ├── raquete.py&emsp;&emsp;&emsp;&emsp;# Classe Raquete <br/>
│   └── jogo.py&emsp;&emsp;&emsp;&emsp;&emsp; # Lógica principal do jogo <br/>
├── Qlearning/&emsp;&emsp; &emsp; &emsp; # Diretório relacionado ao Aprendizado Por Reforço<br/>
│   ├── episodios/&emsp;&emsp;&emsp;&emsp;# Diretório para salvar o agente ao final dos episódios de treino<br/>
│   ├── __init__.py<br/>
│   └── Qlearning.py&emsp;&emsp;&emsp;# Lógica do agente Q-Learning <br/>
├── main.py &emsp;&emsp;&emsp;&emsp; &emsp; # Ponto de entrada para o jogo <br/>
├── PongGame.py &emsp;&emsp;&emsp;# Classe de controle Visual das telas de cada modo de jogo <br/>
├── treino_ql.py &emsp;&emsp;&emsp;&emsp;# Ponto de entrada para o treinamento do agente Q-Learning <br/>
├── treino_ann.py &emsp;&emsp;&emsp; # Ponto de entrada para o treinamento dos individuos da Rede Neural Artificial <br/>
├── requirements.txt &emsp;&emsp;# Arquivo contendo as depencências do projeto <br/>
└── README.md &emsp; &emsp; &emsp;# Este arquivo <br/>

## Dependências
- Python 3.11.5
- numpy 1.26.4
- pygame 2.5.2
