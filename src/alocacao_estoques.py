import copy
import math
import random
from datetime import datetime
from itertools import chain


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


def alocacao_reservas(
    estoque: Estoque, reservas: list[Reserva], probabilidade: float
) -> Estoque:

    estoque = copy.deepcopy(estoque)

    while reservas:
        reserva = reservas.pop()
        loop_corredores = True
        precisa_dividir = False

        while loop_corredores:
            divisivel = False
            if precisa_dividir:
                divisivel = True
            precisa_dividir = True

            for corredor in chain.from_iterable(estoque):
                item = reserva["item"]
                quantidade = reserva["quantidade"]
                espaco = corredor["disponivel"][item]

                tem_espaco = espaco >= quantidade
                if tem_espaco:
                    precisa_dividir = False

                if random.random() > probabilidade:
                    continue

                if not tem_espaco:
                    if not divisivel:
                        continue

                    if espaco == 0:
                        continue

                    nova_reserva = copy.deepcopy(reserva)
                    nova_reserva["quantidade"] = quantidade - espaco
                    reservas.append(nova_reserva)
                    reserva["quantidade"] = espaco
                    quantidade = espaco

                corredor["disponivel"][item] -= quantidade
                corredor["reservas"].append(reserva)
                loop_corredores = False
                break

    return estoque


def calcula_funcao_objetivo(
    estoque: Estoque, peso_distancia: float, peso_andar: float
) -> float:

    def x(corredor: int):
        return math.ceil(corredor / 2)

    corredores_andares = dict()
    for a, andar in enumerate(estoque):
        for c, corredor in enumerate(andar, start=1):
            for reserva in corredor["reservas"]:
                onda = reserva["onda"]
                if onda not in corredores_andares:
                    corredores_andares[onda] = dict()

                if a not in corredores_andares[onda]:
                    corredores_andares[onda][a] = {
                        "mais_distante": 0,
                        "menos_distante": float("inf"),
                        "num_corredores": 0,
                        "corredores_vistos": [],
                    }

                corredor_dict = corredores_andares[onda][a]

                dist = "mais_distante"
                corredor_dict[dist] = max(corredor_dict[dist], x(c))

                mdist = "menos_distante"
                corredor_dict[mdist] = min(corredor_dict[mdist], x(c))

                if c not in corredor_dict["corredores_vistos"]:
                    corredor_dict["corredores_vistos"].append(c)
                    corredor_dict["num_corredores"] += 1

    funcao_objetivo = 0
    for onda in corredores_andares.values():
        for andar in onda.values():
            funcao_objetivo += (
                andar["mais_distante"] - andar["menos_distante"]
            ) * peso_distancia

            funcao_objetivo += andar["num_corredores"]

        funcao_objetivo += len(onda) * peso_andar

    return funcao_objetivo

