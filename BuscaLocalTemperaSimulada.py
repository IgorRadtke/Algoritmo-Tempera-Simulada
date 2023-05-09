from socket import timeout
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
        self.temperatura : int = 1
        #self.temperatura = 1

        # Configura a velocidade de resfriamento
        self.alpha = alpha
        
        self.estrategia_resfriamento = estrategia_resfriamento

        # Configura a estratégia de resfriamento

        self.resfriamento = lambda t: t * self.alpha if self.estrategia_resfriamento == 1 else t - self.alpha if t - self.alpha >= 0 else 0

        # self.resfriamento = lambda t: t * self.alpha if self.estrategia_resfriamento == 1 else lambda t: t - self.alpha if t - self.alpha >= 0 else lambda t: 0

        # Define a solução inicial
        self.solucao = self.gerar_solucao_inicial_aleatoria() if solucao_inicial is None else solucao_inicial




    # Executa a busca local com tempera simulada
    # Retorna uma lista de soluções
    def buscar_solucao(self) -> list[Solucao]:
        

        # Regra da probabilidade
        probabilidade = lambda delta, temperatura: math.exp(-delta / temperatura) if temperatura > 0 else 0

        # Razão entre o custo do vizinho e o custo atual(pivô)
        delta = lambda custo_vizinho, custo_pivo: custo_vizinho / custo_pivo - 1




        # Condições de parada:
            # 1 - A solução atual (pivô) é a solução ótima
            # 2 - A solução atual (pivô) não sofreu alteração
            # 3 - O tempo limite foi atingido



        solucoes = [self.solucao]                       # Lista de soluções geradas   
        solucao_pivo = self.solucao

        iteracao = self.solucao.iteracao + 1

        # Valida as condições de parada: solução ótima, tempo limite
        while solucao_pivo.qualidade != self.solucao_otima or time.time() < self.tempo_limite:

            iteracao += 1
            
            solucao_vizinha = self.vizinhanca.proximo_vizinho(self.solucao, self.solucao.i_movimento, self.solucao.j_movimento+1)

            # Computa a variação de custo
            
            if (delta(solucao_vizinha.qualidade, solucao_pivo.qualidade) < 0): # Aceita a solução vizinha
                
                self.solucao = solucao_vizinha                          # Atualiza a solução atual
                self.solucao.iteracao = iteracao                        # Atualiza a iteração
                self.solucao.tempo = time.time() - self.tempo_limite    # Atualiza o tempo

                solucoes.append(self.solucao)                           # Armazena a solução atual na lista de soluções
                
                # Minha solução vira o pivô
                solucao_pivo = self.solucao
                
            else: # Verifica a probabilidade de aceitação da solução vizinha
                #print("tipo temperatura: " + str(type(self.temperatura)))
                if (random.random() < probabilidade(delta(solucao_vizinha.qualidade, solucao_pivo.qualidade), self.temperatura )):
                    
                    solucao_pivo = solucao_vizinha                          # Minha solução vira o pivô
                    self.solucao.tempo = time.time() - self.tempo_limite    # Atualiza o tempo
                    
                    
            atualiza_j = lambda j, ciclo: j+1 if j < len(ciclo) else 0      # Atualiza o j para o próximo vizinho
            atualiza_i = lambda i, ciclo: i+1 if i < len(ciclo)-1 else 0    # Atualiza o i para o próximo vizinho
            
            if (atualiza_j(self.solucao.j_movimento, self.solucao.ciclo) == 0):
                if (atualiza_i(self.solucao.i_movimento, self.solucao.ciclo) == 0):
                    break
                else:
                    self.solucao.i_movimento = atualiza_i(self.solucao.i_movimento, self.solucao.ciclo)
            else:
                self.solucao.j_movimento = atualiza_j(self.solucao.j_movimento, self.solucao.ciclo)
                
                
                
            # Atualiza a temperatura
            self.temperatura = self.resfriamento(self.temperatura) 

            
        return solucoes


            ### Nossa tentativa de implementação que não deu certo


            # i, j = 0, 1
            # while self.vizinhanca.proximo_vizinho(solucao_pivo, i, j):

            #     # Gera uma nova solução vizinha
            #     solucao_vizinha = self.vizinhanca.proximo_vizinho(solucao_pivo, i, j)

            #     # Computa a variação de custo
            #     variacao_de_custo = delta(solucao_vizinha.qualidade, solucao_pivo.qualidade)


            #     # Verificações para aceitação da solução vizinha
            #     if variacao_de_custo <= 0:
            #         solucao_pivo = solucao_vizinha
            #         pivo_alterado = True
            #     else:
            #         if random.random() < probabilidade(variacao_de_custo, self.temperatura):
            #             solucao_pivo = solucao_vizinha
            #             pivo_alterado = True



            #     # Se o pivo foi alterado, então faz as atualizações necessárias
            #     if pivo_alterado:
            #         # Resfria a temperatura
            #         self.temperatura = self.resfriamento(self.temperatura)

            #         # Atualiza a melhor solução
            #         if solucao_pivo.qualidade < melhor_solucao.qualidade:
            #             melhor_solucao = solucao_pivo
                    
            #         # Armazena a solução atual na lista de soluções
            #         solucoes.append(solucao_pivo)

            #         # Pula para a próxima iteração
            #         break




            #     # Atualiza os indices para busca na vizinhança
            #     j += 1
            #     if j == self.vizinhanca.tamanho:
            #         i += 1
            #         j = i + 1
            

            
            # # Se o pivo não foi alterado na iteração, então não há mais vizinhos encerra a busca
            # if not pivo_alterado:
            #     break