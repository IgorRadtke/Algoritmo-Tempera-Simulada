import csv
import statistics
import time
import os.path

from Vizinhanca2opt import Vizinhanca2opt
from BuscaHibridaGulosoTemperaSimulada import BuscaHibridaGulosoTemperaSimulada


def ler_arquivo(instancia: str) -> tuple:
    with open('instancias/' + instancia + '.csv', 'r') as arquivo:
        leitor = csv.reader(arquivo, quoting=csv.QUOTE_NONNUMERIC, delimiter=",")
        distancias = tuple(map(tuple, leitor))
        return distancias


def computar_metricas(resultados_amostras: list) -> tuple[int, float, int]:
    qualidades, tempos = zip(*resultados_amostras)
    qualidade_media, tempo_medio = sum(qualidades) / amostras, sum(tempos) / amostras
    qualidade_desvio = statistics.stdev(qualidades, qualidade_media)
    qualidade_media, qualidade_desvio, tempo_medio = round(qualidade_media), round(qualidade_desvio, 2), round(tempo_medio)
    return qualidade_media, qualidade_desvio, tempo_medio


def escrever_resultados(resultados: tuple) -> None:
    arquivo_existe = os.path.isfile('resultados.csv')
    with open('resultados.csv', 'a', encoding='UTF8', newline='') as csvf:
        writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not arquivo_existe:
            writer.writerow(cabecalho)
        for i in resultados:
            writer.writerow(i)


def escrever_resultados_amostras(resultados: list) -> None:
    arquivo_existe = os.path.isfile('resultados_amostras.csv')
    with open('resultados_amostras.csv', 'a', encoding='UTF8', newline='') as csvf:
        writer = csv.writer(csvf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not arquivo_existe:
            writer.writerow(cabecalho)
        writer.writerow(resultados)


# Constantes/Parâmetros Fixos
cabecalho = ("instancia", "autoria", "algoritmo", "q-medio", "q-desvio", "t-medio")
arquivos = ('wi29', 'dj38', 'qa194', 'uy734', 'zi929')
#arquivos = ('zi929',)
instancias = ("Western Sahara", "Djibouti", "Qatar", "Uruguay", "Zimbabwe")
#instancias = ("Zimbabwe",)
solucoes_otimas = (27603, 6656, 9352, 79114, 95345)
#solucoes_otimas = (95345,)
amostras = 10
parametro_mandato = 5  # tamanho da instância / parâmetro mandato - busca tabu
parametro_alfa = 0.1  # 30% - guloso-alfa
parametro_tempo = 0.06  # segundos * tamanho instância
autoria = "FG"

# Estratégias de resfriamento
ESTR_RESFRIAMENTO_LINEAR = 0 
ESTR_RESFRIAMENTO_GEOMETRICO = 1 

# Para a progressão geométrica: 0,5 < α < 1
# Para a progressão linear: 0 < α < 0,1
ALPHA = 0.05

# Solução inicial para Busca Local Tempera Simulada
SOLUCAO_INICIAL = 1



def main():
    for idx, arquivo in enumerate(arquivos):
        distancias = ler_arquivo(arquivo)
        tamanho = len(distancias)
        solucao_otima = solucoes_otimas[idx]
        algoritmos = (
            BuscaHibridaGulosoTemperaSimulada(Vizinhanca2opt(distancias), solucao_otima, ESTR_RESFRIAMENTO_LINEAR, ALPHA),
            )
        tempo_limite = tamanho * parametro_tempo
        print("Instância:", instancias[idx])
        for algoritmo_busca in algoritmos:
            print("Algoritmo:", algoritmo_busca.nome)
            resultados = []
            resultados_amostras = [algoritmo_busca.nome]
            for am in range(amostras):
                print("Executando amostra:", am + 1)
                # Início da busca heurística
                tempo_inicial = time.time()
                algoritmo_busca.tempo_limite = tempo_limite + tempo_inicial
                solucao_list = algoritmo_busca.buscar_solucao()
                # Trecho usado para salvar todas os resultados intermediários
                #for solucao in solucao_list:
                #    resultados.append((instancias[idx], algoritmo_busca.nome, solucao.qualidade, tempo_limite + solucao.tempo + 0.000001, solucao.iteracao))
                #escrever_resultados(resultados)

                # Trecho usado para salvar no padrão das atividades
                # print("Lista de Soluções Geradas:" + str(solucao_list))

                # for i in range(len(solucao_list)):
                #     print("Solução " + str(i) + ": " + str(solucao_list[i].qualidade) + " " + str(solucao_list[i].tempo) + " " + str(solucao_list[i].iteracao))
                melhor_qualidade = solucao_list[-1].qualidade
                tempo_execucao = time.time() - tempo_inicial
                resultados.append((melhor_qualidade, tempo_execucao))
                # Trecho usado para salvar amostras independentes
                resultados_amostras.append(melhor_qualidade)

            qualidade_media, qualidade_desvio, tempo_medio = computar_metricas(resultados)
            escrever_resultados(((instancias[idx], autoria, algoritmo_busca.nome, qualidade_media, qualidade_desvio, tempo_medio),))

            # Trecho usado para salvar amostras independentes
            escrever_resultados_amostras(resultados_amostras)


# Rotina de Execução
main()
