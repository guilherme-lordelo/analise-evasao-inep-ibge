# src/inep/uniao/executar_uniao.py
from utils.io import read_csv, write_csv
from utils.paths import PROCESSED_INEP, AGREGACOES

from inep.config import (
    PARES,
    EVASAO_PREFIXO_OUT,
    EVASAO_EXT_OUT,
    UNIAO_ARQ_MUNICIPIOS,
    UNIAO_ARQ_ESTADOS,
    UNIAO_ARQ_BRASIL,
)

from inep.uniao.uniao_municipios import unir_municipios
from inep.uniao.agregacao_estadual import agregar_estadual
from inep.uniao.agregacao_nacional import agregar_nacional


def executar_uniao():
    lista_dfs = []

    # ----------------------
    # 1) Carregar cada par de evasão
    # ----------------------
    for par in PARES:
        ano_p, ano_n = par.split("_")

        nome_arq = f"{EVASAO_PREFIXO_OUT}{ano_p}_{ano_n}{EVASAO_EXT_OUT}"
        caminho = PROCESSED_INEP / nome_arq

        print(f"Lendo {caminho.name}...")
        df = read_csv(caminho)

        lista_dfs.append(df)

    # ----------------------
    # 2) União municipal
    # ----------------------
    print("Unindo pares por município...")
    df_mun = unir_municipios(lista_dfs)

    out_mun = AGREGACOES / UNIAO_ARQ_MUNICIPIOS
    print(f"Salvando {out_mun.name}...")
    write_csv(df_mun, out_mun)

    # ----------------------
    # 3) Agregação estadual
    # ----------------------
    print("Agregando nível estadual...")
    df_uf = agregar_estadual(df_mun)

    out_uf = AGREGACOES / UNIAO_ARQ_ESTADOS
    print(f"Salvando {out_uf.name}...")
    write_csv(df_uf, out_uf)

    # ----------------------
    # 4) Agregação nacional
    # ----------------------
    print("Agregando nível nacional...")
    df_br = agregar_nacional(df_uf)

    out_br = AGREGACOES / UNIAO_ARQ_BRASIL
    print(f"Salvando {out_br.name}...")
    write_csv(df_br, out_br)

    print("União final concluída!")


if __name__ == "__main__":
    executar_uniao()