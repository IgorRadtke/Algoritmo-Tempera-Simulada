from AlgoritmoBusca import AlgoritmoBusca
from Solucao import Solucao
from Vizinhanca import Vizinhanca
from BuscaConstrutivaGulosa import BuscaConstrutivaGulosa
from BuscaLocalTemperaSimulada import BuscaLocalTemperaSimulada
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



    def buscar_solucao(self) -> list[Solucao]:

        guloso = BuscaConstrutivaGulosa(self.distancias, self.solucao_otima)
        guloso.tempo_limite = self.tempo_limite
        solucoes_guloso = guloso.buscar_solucao()

        self.solucao = solucoes_guloso[0]


        solucoes = []
        solucoes.extend(solucoes_guloso)


        tempera_simulada = BuscaLocalTemperaSimulada(self.vizinhanca, self.solucao_otima, self.resfriamento, self.alpha, self.solucao)
        tempera_simulada.tempo_limite = self.tempo_limite
        solucoes_tempera_simulada = tempera_simulada.buscar_solucao()
        solucoes.extend(solucoes_tempera_simulada)

        return solucoes
        
