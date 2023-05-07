from AlgoritmoBusca import AlgoritmoBusca
from Vizinhanca import Vizinhanca
from Solucao import Solucao
import time
import math
import random

class BuscaLocalTemperaSimulada(AlgoritmoBusca):

    # Construtor
    def __init__(self, vizinhanca: Vizinhanca, solucao_otima: int, estrategia_resfriamento: int, alpha: float, solucao_inicial: Solucao = None):

        # Chama o construtor da classe pai
        super().__init__( "BLTS" + vizinhanca.nome, vizinhanca.distancias, solucao_otima )

        # Define a vizinhança
        # Vizinhança2OPT
        self.vizinhanca = vizinhanca

        # Define a temperatura inicial
        self.temperatura = 1

        # Configura a velocidade de resfriamento
        self.alpha = alpha

        # Configura a estratégia de resfriamento
        self.resfriamento = lambda t: t * alpha if estrategia_resfriamento == 1 else lambda t: t - alpha if t - alpha >= 0 else lambda t: 0

        # Define a solução inicial
        self.solucao : Solucao
        self.solucao = self.gerar_solucao_inicial_aleatoria() if solucao_inicial is None else solucao_inicial




    # Executa a busca local com tempera simulada
    # Retorna uma lista de soluções
    def buscar_solucao(self) -> list[Solucao]:

        # Regra da probabilidade
        probabilidade = lambda delta, temperatura: math.exp(-delta / temperatura)

        # Razão entre o custo do vizinho e o custo atual(pivô)
        delta = lambda custo_vizinho, custo_pivo: custo_vizinho / custo_pivo - 1




        # Condições de parada:
            # 1 - A solução atual (pivô) é a solução ótima
            # 2 - A solução atual (pivô) não sofreu alteração
            # 3 - O tempo limite foi atingido



        solucoes = []                       # Lista de soluções geradas   
        solucao_pivo = self.solucao
        solucoes.append(solucao_pivo)       # Adiciona a solução inicial
        melhor_solucao = solucao_pivo
        iteracao = 0

        # Valida as condições de parada: solução ótima, tempo limite
        while melhor_solucao.qualidade != self.solucao_otima or time.time() < self.tempo_limite:

            iteracao += 1

            # Controla se o pivo sofreu alteração
            pivo_alterado = False

            # # Percorre a vizinhança para encontrar a melhor solução
            # for i in range(0, self.vizinhanca.tamanho - 1):
            #     for j in range(i+1, self.vizinhanca.tamanho):
            #         solucao_vizinha = self.vizinhanca.proximo_vizinho(solucao_pivo, i, j)


            i, j = 0, 1
            while self.vizinhanca.proximo_vizinho(solucao_pivo, i, j):

                # Gera uma nova solução vizinha
                solucao_vizinha = self.vizinhanca.proximo_vizinho(solucao_pivo, i, j)

                # Computa a variação de custo
                variacao_de_custo = delta(solucao_vizinha.qualidade, solucao_pivo.qualidade)


                # Verificações para aceitação da solução vizinha
                if variacao_de_custo <= 0:
                    solucao_pivo = solucao_vizinha
                    pivo_alterado = True
                else:
                    if random.random() < probabilidade(variacao_de_custo, self.temperatura):
                        solucao_pivo = solucao_vizinha
                        pivo_alterado = True



                # Se o pivo foi alterado, então faz as atualizações necessárias
                if pivo_alterado:
                    # Resfria a temperatura
                    self.temperatura = self.resfriamento(self.temperatura)

                    # Atualiza a melhor solução
                    if solucao_pivo.qualidade < melhor_solucao.qualidade:
                        melhor_solucao = solucao_pivo
                    
                    # Armazena a solução atual na lista de soluções
                    solucoes.append(solucao_pivo)

                    # Pula para a próxima iteração
                    break




                # Atualiza os indices para busca na vizinhança
                j += 1
                if j == self.vizinhanca.tamanho:
                    i += 1
                    j = i + 1
            

            
            # Se o pivo não foi alterado na iteração, então não há mais vizinhos encerra a busca
            if not pivo_alterado:
                break


        return solucoes