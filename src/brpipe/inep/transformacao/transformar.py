from brpipe.inep.transformacao.calculo import orquestrar_calculo
from brpipe.inep.transformacao.integracao import orquestrar_integracao

def transformar_inep(formato: str = "long"):
    """
    Executa a transformação dos dados INEP.

    Parâmetros:
    - formato: "wide" ou "long" para o formato de saída desejado.

    Retorna:
    - Dicionário de DataFrames transformados.
    """

    # Integração dos dados
    dfs_agregados = orquestrar_integracao(formato)

    if dfs_agregados is None:
        raise ValueError("A agregação retornou None.")

    # Cálculo de métricas
    dfs_calculados = orquestrar_calculo(dfs_agregados, formato=formato)

    if dfs_calculados is None:
        raise ValueError("O cálculo retornou None.")

    return dfs_calculados