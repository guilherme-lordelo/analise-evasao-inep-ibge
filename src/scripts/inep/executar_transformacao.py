from inep.transformacao.calculo import orquestrar_calculo
from inep.transformacao.integracao import orquestrar_integracao
from inep.carga import salvar_resultados


def executar_transformacao():
    dfs_agregados = orquestrar_integracao("wide")

    if dfs_agregados is None:
        raise ValueError("A agregação retornou None.")

    dfs_calculados = orquestrar_calculo(dfs_agregados)

    if dfs_calculados is None:
        raise ValueError("O cálculo retornou None.")

    salvar_resultados(dfs_calculados)


if __name__ == "__main__":
    executar_transformacao()
