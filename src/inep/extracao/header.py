from utils.io import read_header
from inep.config import VARIAVEIS, COL_MAPPINGS

def ler_header(path):
    return read_header(path)

def detectar_mapeamento(header):
    return {col: destino for col, destino in COL_MAPPINGS.items() if col in header}

def determinar_colunas_existentes(header, mapeamento):
    colunas = []

    for var in VARIAVEIS:
        if var in header:
            colunas.append(var)
        elif var in mapeamento.values():
            chave_original = [k for k, v in mapeamento.items() if v == var][0]
            if chave_original in header:
                colunas.append(chave_original)

    return colunas

def identificar_faltantes(colunas_existentes, mapeamento):
    return set(VARIAVEIS) - {
        mapeamento.get(c, c) for c in colunas_existentes
    }
