import pandas as pd
from brpipe.inep.config import VARIAVEIS_YAML

def padronizar_categoricas(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    """
    Cria dummies para variáveis categóricas seguindo o padrão: VARIAVEL_VALOR_ANO
     - VARIAVEL sendo a variável categórica
     - VALOR são os valores previstos no YAML ou 'OUTROS'
     - ANO é o ano fornecido como argumento

    A função assume que as colunas categóricas já foram renomeadas
    para o padrão VARIAVEL_{ano}.
    """

    df_out = df.copy()
    sufixo = f"_{ano}"

    # Padroniza cada variável categórica
    for var in VARIAVEIS_YAML.categoricas:

        col_ano = f"{var}{sufixo}"
        if col_ano not in df_out.columns:
            # variável não encontrada, pula
            continue

        # Valores válidos segundo o YAML
        valores_validos = VARIAVEIS_YAML.valores_categoricos[var]

        # Mapeia OUTROS
        serie = df_out[col_ano].apply(
            lambda x: x if x in valores_validos else "OUTROS"
        )

        # Cria dummies
        dummies = pd.get_dummies(
            serie,
            prefix=f"{var}",
            prefix_sep="_",
            dtype=float
        )

        # Ajusta nomes para incluir o ano
        dummies = dummies.rename(
            columns={c: f"{c}{sufixo}" for c in dummies.columns}
        )

        # Adiciona ao dataframe
        df_out = pd.concat([df_out, dummies], axis=1)

        # Remove a coluna original categórica
        df_out.drop(columns=[col_ano], inplace=True)

    return df_out
