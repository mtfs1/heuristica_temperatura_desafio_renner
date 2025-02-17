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


type Caixa = int
type Item = int
type Onda = int

class Reserva(dict):
    caixa: Caixa
    item: Item
    quantidade: QuantidadeItem
    onda: Onda


def gera_documentos_reservas(
    caixas: list[tuple[Lote, int]], num_ondas: int, limite_onda: int
) -> list[Reserva]:
    print(f"[{datetime.now()}][GERA DOCUMENTOS RESERVAS]")

    ondas = [
        {"quantidade": 0, "classe": None} for _ in range(num_ondas)
    ]
    reservas = []
    for c, (caixa, classe_onda) in enumerate(caixas):
        #TODO: criar algoritmo imune a fagmentacao
        onda_caixa = None
        tamanho_caixa = sum(caixa)
        for o, onda in enumerate(ondas):
            if onda["quantidade"] + tamanho_caixa > limite_onda:
                continue

            if not onda["classe"] in [None, classe_onda]:
                continue

            onda["classe"] = classe_onda
            onda["quantidade"] += tamanho_caixa
            onda_caixa = o
            break

        if onda_caixa == None:
            print("[ERROR][NAO PODE ACHAR ONDA PARA CAIXA]")
            exit(1)

        for item, quantidade in enumerate(caixa):
            if quantidade == 0:
                continue

            reserva = {
                "caixa": c,
                "item": item,
                "quantidade": quantidade,
                "onda": onda_caixa,
            }
            reservas.append(reserva)

    return reservas

