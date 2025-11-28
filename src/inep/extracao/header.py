from utils.io import read_csv
from inep.config import SEP, ENCODING, VARIAVEIS

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
    """
    Retorna todas as colunas existentes no arquivo, considerando
    as variáveis definidas no YAML e o mapeamento.
    """
    colunas = []

    for var in VARIAVEIS:
        # Caso 1: a coluna existe com o nome original
        if var in header:
            colunas.append(var)

        # Caso 2: existe renomeamento
        elif var in mapeamento.values():
            chave_original = [k for k, v in mapeamento.items() if v == var][0]
            if chave_original in header:
                colunas.append(chave_original)

    return colunas


def identificar_faltantes(colunas_existentes, mapeamento):
    return set(VARIAVEIS) - {
        mapeamento.get(c, c) for c in colunas_existentes
    }
