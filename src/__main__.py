from datetime import datetime

from alocacao_estoques import alocacao_reservas
from alocacao_estoques import calcula_funcao_objetivo
from alocacao_estoques import gera_documentos_reservas
from alocacao_estoques import gera_estrutura_estoque
from alocacao_estoques import retira_reservas
from gera_dados_entrada import dados_de_caixas, dados_de_estoque


def main():
    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][START]")

    estoque = dados_de_estoque()
    caixas = dados_de_caixas()
    estoque = gera_estrutura_estoque(estoque)
    reservas = gera_documentos_reservas(caixas, 1, 6000)

    estoque = alocacao_reservas(estoque, reservas, 0.5)
    objetivo = calcula_funcao_objetivo(estoque, 1, 1)

    temperaturas = [
        {
            "probabilidade": 0.7,
            "vezes": 100,
        },
        {
            "probabilidade": 0.4,
            "vezes": 200,
        },
        {
            "probabilidade": 0.2,
            "vezes": 400,
        },
    ]

    print(f"[{datetime.now()}][SCORE][{objetivo}]")
    for temperatura in temperaturas:
        for _ in range(temperatura["vezes"]):
            novo_estoque, retiradas = retira_reservas(
                estoque, temperatura["probabilidade"]
            )
            novo_estoque = alocacao_reservas(novo_estoque, retiradas, 0.5)
            novo_objetivo = calcula_funcao_objetivo(novo_estoque, 1, 1)

            if novo_objetivo < objetivo:
                objetivo = novo_objetivo
                estoque = novo_estoque
                print(f"[{datetime.now()}][SCORE][{objetivo}]")

    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][END]")

if __name__ == "__main__":
    main()

