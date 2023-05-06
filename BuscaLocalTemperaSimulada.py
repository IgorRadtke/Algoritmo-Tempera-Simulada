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

        solucoes = []                       # Lista de soluções geradas   
        solucoes.append(self.solucao)       # Adiciona a solução inicial


        # Regra da probabilidade
        probabilidade = lambda delta, temperatura: math.exp(-delta / temperatura) if temperatura > 0 else 1

        # Razão entre o custo do vizinho e o custo atual(pivô)
        delta = lambda custo_vizinho, custo_atual: custo_vizinho / custo_atual - 1

        # Condições de parada:
            # 1 - A solução atual (pivô) é a solução ótima
            # 2 - A solução atual (pivô) não sofreu alteração
            # 3 - O tempo limite foi atingido

 
        # Gera uma solução vizinha

        i, j = 0, 1
        solucao_vizinha = self.vizinhanca.proximo_vizinho(self.solucao, i, j)   # Gera uma nova solução vizinha


        counter = 0
        while self.solucao.qualidade != self.solucao_otima or self.solucao.qualidade == solucao_vizinha.qualidade or time.time() < self.tempo_limite:

            # Se a solução vizinha for melhor que a solução atual, ou se a probabilidade for maior que um número aleatório, então a solução atual é substituída pela solução vizinha
            ### VALIDAR SE É ASSIM QUE FUNCIONA !!!!!!!!!!!!
            if solucao_vizinha.qualidade < self.solucao.qualidade or random.random() < probabilidade(delta(solucao_vizinha.qualidade, self.solucao.qualidade), self.temperatura):
                self.solucao.tempo = time.time() - self.tempo_limite    # Armazena o tempo de execução
                self.solucao.iteracao = counter                         # Armazena o número de iterações
                self.solucao = solucao_vizinha                          # Substitui a solução atual pela solução vizinha
            else: 
                break


            solucoes.append(self.solucao)                                   # Adiciona a solução atual na lista de soluções
            self.temperatura = self.resfriamento(self.temperatura)          # Resfria a temperatura
            counter += 1                                                    # Incrementa o contador de iterações
            solucao_vizinha = self.vizinhanca.proximo_vizinho(self.solucao, i+1, j+1)   # Gera uma nova solução vizinha

        return solucoes


            





    


