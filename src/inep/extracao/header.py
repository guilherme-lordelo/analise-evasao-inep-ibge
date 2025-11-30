from inep.config import SEP, ENCODING, VARIAVEIS, COL_MAPPINGS

def ler_header(path):
    with open(path, "r", encoding=ENCODING) as f:
        header = f.readline().strip().split(SEP)
    return header


def detectar_mapeamento(header):
    return {col: destino for col, destino in COL_MAPPINGS.items() if col in header}


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
