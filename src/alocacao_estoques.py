from datetime import datetime


type QuantidadeItem = int
type Lote = list[QuantidadeItem]

class Corredor(dict):
    estoque: Lote
    disponivel: Lote
    reservas: list

type Andar = list[Corredor]
type Estoque = list[Andar]


def gera_estrutura_estoque(estoque: list) -> Estoque:
    print(f"[{datetime.now()}][GERA EXTRUTURA DE ESTOQUE]")

    estrutura_estoque = []
    for andar in estoque:
        estrutura_estoque.append([])
        for corredor in andar:
            estrutura_estoque[-1].append(dict())
            estrutura_estoque[-1][-1]["estoque"] = corredor[:]
            estrutura_estoque[-1][-1]["disponivel"] = corredor[:]
            estrutura_estoque[-1][-1]["reservas"] = []

    return estrutura_estoque


