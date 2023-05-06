from AlgoritmoBusca import AlgoritmoBusca
from Solucao import Solucao
from Vizinhanca import Vizinhanca
from BuscaConstrutivaGulosa import BuscaConstrutivaGulosa
from BuscaLocalTemperaSimulada import buscar_solucao as buscaLocalTemperaSimulada
import time

class BuscaHibridaGulosoTemperaSimulada(AlgoritmoBusca):

    # Construtor
    def __init__(self, vizinhanca: Vizinhanca, solucao_otima: int, estrategia_resfriamento: int, alpha: float):
        
        # Chama o construtor da classe pai
        super().__init__("CG+PM"+vizinhanca.nome, vizinhanca.distancias, solucao_otima)

        # Define a vizinhança
        self.vizinhanca = vizinhanca

        # Define a temperatura inicial
        self.temperatura = 1

        # Configura a velocidade de resfriamento
        self.alpha = alpha

        # Configura a estratégia de resfriamento
        self.resfriamento = lambda t: t * alpha if estrategia_resfriamento == 1 else lambda t: t - alpha if t - alpha >= 0 else lambda t: 0

        # Define a solução inicial usando o algoritmo guloso
        self.solucao = BuscaConstrutivaGulosa(vizinhanca.distancias, solucao_otima).buscar_solucao()[0]

    # Executa a busca local com tempera simulada



    # Importar somente a função buscar_solucao da classe BuscaLocalTemperaSimulada
    # não sei se isso funciona :)
    def buscar_solucao(self) -> list[Solucao]:
        buscaLocalTemperaSimulada(self)
        
