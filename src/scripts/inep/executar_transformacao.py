from inep.transformacao.calculo import orquestrar_calculo
from inep.transformacao.integracao import orquestrar_integracao
from inep.carga import salvar_resultados


def executar_transformacao():

    TIPO_FORMATO = "long"  # "wide" ou "long"
    dfs_agregados = orquestrar_integracao(TIPO_FORMATO)

    if dfs_agregados is None:
        raise ValueError("A agregação retornou None.")

    dfs_calculados = orquestrar_calculo(dfs_agregados, formato=TIPO_FORMATO)

    if dfs_calculados is None:
        raise ValueError("O cálculo retornou None.")

    salvar_resultados(dfs_calculados)


if __name__ == "__main__":
    executar_transformacao()
