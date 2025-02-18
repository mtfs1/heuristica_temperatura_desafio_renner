import os
from datetime import datetime

import pandas as pd


dir_arquivos = os.path.join(
    os.path.dirname(__file__),
    "..",
    "arquivos",
)


def enumera(df: pd.DataFrame, coluna: str) -> dict:
    return {
        val: i
        for i, val in enumerate(df[coluna].sort_values().unique())
    }


def transforma_dados_de_entrada(
    estoque: pd.DataFrame, caixas: pd.DataFrame
) -> tuple[list, list]:
    print(f"[{datetime.now()}][TRANSFORMA DADOS DE ENTRADA]")

    todos_os_itens = pd.concat(
        [estoque[["SKU"]], caixas[["SKU"]]],
        ignore_index=True
    )
    itens = enumera(todos_os_itens, "SKU")

    E = dados_de_estoque(estoque, itens)
    C = dados_de_caixas(caixas, itens)

    return E, C


def dados_de_estoque(estoque: pd.DataFrame, itens: dict) -> list:
    print(f"[{datetime.now()}][DADOS DE ESTOQUE]")

    andares = enumera(estoque, "ANDAR")
    corredores = enumera(estoque, "CORREDOR")

    E = [
        [[0 for _ in itens] for _ in corredores]
        for _ in andares
    ]

    for _, linha in estoque.iterrows():
        andar = andares[linha["ANDAR"]]
        corredor = corredores[linha["CORREDOR"]]
        item = itens[linha["SKU"]]
        E[andar][corredor][item] = linha["PECAS"]

    return E


def dados_de_caixas(caixas: pd.DataFrame, itens: dict) -> list:
    print(f"[{datetime.now()}][DADOS DE CAIXAS]")

    ids = enumera(caixas, "CAIXA_ID")
    classes = enumera(caixas, "CLASSE_ONDA")

    C = [[[0 for _ in itens], 0] for _ in ids]

    for _, linha in caixas.iterrows():
        id = ids[linha["CAIXA_ID"]]
        classe = classes[linha["CLASSE_ONDA"]]
        item = itens[linha["SKU"]]
        C[id][0][item] = linha["PECAS"]
        C[id][1] = classe

    return C

