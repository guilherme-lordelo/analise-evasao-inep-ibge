# utils/substituicao.py

def substituir_pn(expressao: str, ano_base: str, ano_seguinte: str) -> str:
    """
    Substitui {p} pelo ano_base e {n} pelo ano_seguinte.
    """
    if not isinstance(expressao, str):
        return expressao

    return (
        expressao.replace("{p}", str(ano_base))
                 .replace("{n}", str(ano_seguinte))
    )
