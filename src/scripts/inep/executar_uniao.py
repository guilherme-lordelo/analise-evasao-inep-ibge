from utils.paths import DATA_PROCESSED
from utils.io import write_csv

from inep.uniao.carregamento_pares import ler_pares_evasao, merge_pares
from inep.uniao.validacao import separar_validos_invalidos
from inep.uniao.ponderacao import calcular_media_ponderada
from inep.uniao.agregacao import agrega_evasao

import pandas as pd


def main():
    # 1. LER E MERGEAR
    dfs = ler_pares_evasao()
    evasao_all = merge_pares(dfs)

    # 2. VALIDOS / INVALIDOS
    validos, invalidos = separar_validos_invalidos(evasao_all)

    # 3. CÁLCULOS
    validos = calcular_media_ponderada(validos)

    # 4. AGREGAÇÃO
    agregado_uf = agrega_evasao(validos, "SG_UF")
    agregado_br = agrega_evasao(validos.assign(NIVEL="BRASIL"), "NIVEL")
    evasao_agregada = pd.concat([agregado_uf, agregado_br])

    # 5. SALVAR
    write_csv(validos, DATA_PROCESSED / "municipios_evasao_valida_2020_2024.csv", sep=";")
    write_csv(invalidos, DATA_PROCESSED / "municipios_evasao_invalida_2020_2024.csv", sep=";")
    write_csv(evasao_agregada, DATA_PROCESSED / "evasao_uf_e_brasil_2020_2024.csv", sep=";")

    print("Arquivos salvos")


if __name__ == "__main__":
    main()
