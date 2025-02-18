from datetime import datetime

from alocacao_estoques import alocacao_reservas
from alocacao_estoques import calcula_funcao_objetivo
from alocacao_estoques import gera_documentos_reservas
from alocacao_estoques import gera_estrutura_estoque
from gera_dados_entrada import dados_de_caixas, dados_de_estoque


def main():
    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][START]")

    estoque = dados_de_estoque()
    caixas = dados_de_caixas()
    estoque = gera_estrutura_estoque(estoque)
    reservas = gera_documentos_reservas(caixas, 20, 6)

    estoque = alocacao_reservas(estoque, reservas, 0.5)
    objetivo = calcula_funcao_objetivo(estoque, 1, 1)

    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][END]")

if __name__ == "__main__":
    main()

