from datetime import datetime

from gera_dados_entrada import dados_de_caixas, dados_de_estoque


def main():
    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][START]")

    estoque = dados_de_estoque()
    caixas = dados_de_caixas()

    print(f"[{datetime.now()}][HEURISTICA TEMPERATURA][END]")

if __name__ == "__main__":
    main()

