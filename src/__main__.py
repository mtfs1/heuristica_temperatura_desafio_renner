import os
from datetime import datetime

import pandas as pd

from alocacao_estoques import alocacao_reservas
from alocacao_estoques import calcula_funcao_objetivo
from alocacao_estoques import gera_documentos_reservas
from alocacao_estoques import gera_estrutura_estoque
from alocacao_estoques import retira_reservas
from gera_dados_entrada import transforma_dados_de_entrada


dir_arquivos = os.path.join(
    os.path.dirname(__file__),
    "..",
    "arquivos",
)


CAPACIDADE_ONDA = 6000
NUMERO_MAXIMO_ONDAS = 10
PESO_DISTANCIA = 1
PESO_ANDAR = 1
PROBABILIDADE_ALOCACAO_RESERVA = 0.5


def main():
    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][START]")

    print(f"[{datetime.now()}][CARREGA CSV ESTOQUE]")
    estoque = pd.read_csv(
        os.path.join(dir_arquivos, "estoque_selected.csv")
    )

    print(f"[{datetime.now()}][CARREGA CSV CAIXAS]")
    caixas = pd.read_csv(
        os.path.join(dir_arquivos, "caixas_selected.csv")
    )

    estoque, caixas = transforma_dados_de_entrada(estoque, caixas)
    estoque = gera_estrutura_estoque(estoque)
    reservas = gera_documentos_reservas(
        caixas, NUMERO_MAXIMO_ONDAS, CAPACIDADE_ONDA
    )

    estoque = alocacao_reservas(
        estoque, reservas, PROBABILIDADE_ALOCACAO_RESERVA
    )
    objetivo = calcula_funcao_objetivo(estoque, PESO_DISTANCIA, PESO_ANDAR)

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
            novo_estoque = alocacao_reservas(
                novo_estoque, retiradas, PROBABILIDADE_ALOCACAO_RESERVA
            )
            novo_objetivo = calcula_funcao_objetivo(
                novo_estoque, PESO_DISTANCIA, PESO_ANDAR
            )

            if novo_objetivo < objetivo:
                objetivo = novo_objetivo
                estoque = novo_estoque
                print(f"[{datetime.now()}][SCORE][{objetivo}]")

    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][END]")

if __name__ == "__main__":
    main()

