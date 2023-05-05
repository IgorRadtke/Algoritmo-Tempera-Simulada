from AlgoritmoBusca import AlgoritmoBusca
from Vizinhanca import Vizinhanca
from Solucao import Solucao
import time

class SimulatedAnnealing(AlgoritmoBusca):
    def __init__(self, vizinhanca: Vizinhanca, solucao_otima: int, alpha: float, temperatura_inicial: float, resfriamento: float, solucao: Solucao = None):
        super().__init__("SA_" + vizinhanca.nome, vizinhanca.distancias, solucao_otima)