import pygame

from PONG import Jogo


class PongGame:
    def __init__(self, tela, largura, altura):
        self.jogo = Jogo(tela, largura, altura)
        self.bola = self.jogo.bola
        self.raquete_esquerda = self.jogo.raquete_esquerda
        self.raquete_direita = self.jogo.raquete_direita

    def jogada_adversario_perfeito(self):
        acao = self.jogo.adversario_perfeito()
        if acao:
            self.jogo.move_raquetes(esquerda=False, cima=True)
        else:
            self.jogo.move_raquetes(esquerda=False, cima=False)

    def jogar(self):
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

            self.jogada_adversario_perfeito()

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()

    def treina_ann(self, individuo_1):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.jogada_adversario_perfeito()

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

            # Se alguem errar, para o jogo
            if (
                informacao_jogo.pontuacao_dir >= 1
                or informacao_jogo.pontuacao_esq >= 1
                or informacao_jogo.acertos_esq > 50
            ):
                individuo_1.calcula_fitness(
                    informacao_jogo=informacao_jogo,
                )
                run = False

    def jogar_ann(self, individuo):
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
                # distancia_bola=abs(self.raquete_esquerda.x - self.bola.x),
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

    def treina_qlearning(self, agente):
        run = True
        acao = 0
        clock = pygame.time.Clock()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.jogada_adversario_perfeito()

            # -----
            _recompensa = 0

            estado_bola = agente.define_estado(self.raquete_esquerda.y, self.bola.y)
            estado = (estado_bola, acao)

            acao = agente.proxima_acao(estado=estado, treino=True)

            if acao == 1:
                self.jogo.move_raquetes(esquerda=True, cima=False)
            elif acao == 2:
                self.jogo.move_raquetes(esquerda=True, cima=True)

            # Treinamento
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

    def jogar_qlearning(self, agente):
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
            # -----

            informacao_jogo = self.jogo.loop()
            self.jogo.cria_tela(True, False)
            pygame.display.update()

        pygame.quit()
