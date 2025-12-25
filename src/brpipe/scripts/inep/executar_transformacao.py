from brpipe.inep.transformacao import transformar_inep
from brpipe.inep.carga import salvar_resultados


def executar_transformacao():

    TIPO_FORMATO = "long"  # "wide" ou "long"
    dfs_transformados = transformar_inep(TIPO_FORMATO)

    salvar_resultados(dfs_transformados)


if __name__ == "__main__":
    executar_transformacao()
