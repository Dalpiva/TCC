import pygame
from PONG import Jogo


class PongGame:
    def __init__(self, tela: pygame.Surface, largura: int, altura: int) -> None:
        """
        Inicializa a classe PongGame com os parâmetros da tela e as dimensões do jogo.

        Args:
            tela (pygame.Surface): A superfície do jogo onde os elementos são renderizados.
            largura (int): A largura da tela do jogo.
            altura (int): A altura da tela do jogo.
        """
        self.jogo = Jogo(tela, largura, altura)
        self.bola = self.jogo.bola
        self.raquete_esquerda = self.jogo.raquete_esquerda
        self.raquete_direita = self.jogo.raquete_direita

    def mover_raquete_adversario_perfeito(self) -> None:
        """
        Move a raquete do oponente de forma perfeita, calculando se deve se mover para cima ou para baixo
        com base na posição da bola.
        """
        acao = self.jogo.adversario_perfeito()
        if acao:
            self.jogo.move_raquetes(esquerda=False, cima=True)
        else:
            self.jogo.move_raquetes(esquerda=False, cima=False)

    def jogar(self) -> None:
        """
        Inicia o loop principal do jogo Pong, onde o jogador controla a raquete esquerda e um adversário perfeito
        controla a raquete direita.
        """
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

            self.mover_raquete_adversario_perfeito()

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()

    def treinar_ann(self, individuo_1) -> None:
        """
        Treina uma rede neural artificial jogando Pong contra um adversário perfeito.

        Args:
            individuo_1: O indivíduo da rede neural artificial a ser treinado.
        """
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.mover_raquete_adversario_perfeito()

            entrada_1 = individuo_1.cria_entrada(
                raquete_y=self.raquete_esquerda.y,
                bola_y=self.bola.y,
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

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(False, True)
            pygame.display.update()

            if (
                informacao_jogo.pontuacao_dir >= 1
                or informacao_jogo.pontuacao_esq >= 1
                or informacao_jogo.acertos_esq > 50
            ):
                individuo_1.calcula_fitness(
                    informacao_jogo=informacao_jogo,
                )
                run = False

    def jogar_com_ann(self, individuo) -> None:
        """
        Inicia o jogo utilizando uma rede neural artificial para controlar a raquete esquerda.

        Args:
            individuo: O indivíduo da rede neural artificial que controlará a raquete esquerda.
        """
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

    def treinar_com_qlearning(self, agente) -> None:
        """
        Treina um agente utilizando o algoritmo de Q-Learning jogando Pong contra um adversário perfeito.

        Args:
            agente: O agente de Q-Learning a ser treinado.
        """
        run = True
        acao = 0
        clock = pygame.time.Clock()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.mover_raquete_adversario_perfeito()

            _recompensa = 0

            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)
            estado = (estado_bola, acao)

            acao = agente.proxima_acao(estado=estado, treino=True)

            if acao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=False)
            elif acao == 2:
                self.jogo.move_raquetes(esquerda=True, cima=True)

            _recompensa = agente.recebe_recompensa(self.raquete_esquerda.y, self.bola.y)
            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)

            proximo_estado = (estado_bola, acao)
            agente.atualiza_tabela_q(estado, acao, _recompensa, proximo_estado)
            agente.recompensa += _recompensa

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

            if -30 <= _recompensa >= 30:
                print("Treino finalizado; Recompensa: ", _recompensa)
                self.jogo.reset()
                run = False

    def jogar_com_qlearning(self, agente) -> None:
        """
        Inicia o jogo utilizando um agente treinado com Q-Learning para controlar a raquete esquerda.

        Args:
            agente: O agente de Q-Learning que controlará a raquete esquerda.
        """
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

            acao = agente.proxima_acao(estado=estado, treino=False)

            if acao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=False)
            elif acao == 2:
                self.jogo.move_raquetes(esquerda=True, cima=True)

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()
