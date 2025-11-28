from utils.io import read_csv
from inep.config import SEP, ENCODING, COLUNAS_SELECIONADAS


def ler_header(path):
    with open(path, "r", encoding=ENCODING) as f:
        header = f.readline().strip().split(SEP)
    return header


def detectar_mapeamento(header):
    mapeamento = {}

    if "QT_ING" in header and "QT_ING_TOTAL" not in header:
        mapeamento["QT_ING"] = "QT_ING_TOTAL"
    if "QT_MAT" in header and "QT_MAT_TOTAL" not in header:
        mapeamento["QT_MAT"] = "QT_MAT_TOTAL"
    if "QT_CONC" in header and "QT_CONC_TOTAL" not in header:
        mapeamento["QT_CONC"] = "QT_CONC_TOTAL"

    return mapeamento


def determinar_colunas_existentes(header, mapeamento):
    colunas = []
    for c in COLUNAS_SELECIONADAS:
        if c in header:
            colunas.append(c)
        elif c in mapeamento.values():
            chave_original = list(mapeamento.keys())[list(mapeamento.values()).index(c)]
            if chave_original in header:
                colunas.append(chave_original)
    return colunas


def identificar_faltantes(colunas_existentes, mapeamento):
    return set(COLUNAS_SELECIONADAS) - {
        mapeamento.get(c, c) for c in colunas_existentes
    }
