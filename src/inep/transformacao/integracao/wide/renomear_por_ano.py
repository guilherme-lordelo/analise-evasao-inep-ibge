# inep/Transformacao/Integracao/wide/renomear_por_ano.py
from inep.config import VARIAVEIS_YAML

def renomear_com_ano(df, ano: int):
    """
    Renomeia colunas do df no formato:
        variavel -> variavel_{ano}

    Também preenche as variáveis quantitativas
    com 0.0 após o renomeamento.

    Colunas não previstas são ignoradas.
    """
    sufixo = f"_{ano}"
    novo_nome = {}

    for col in df.columns:
        if col in VARIAVEIS_YAML.categoricas or col in VARIAVEIS_YAML.quantitativas:
            novo_nome[col] = f"{col}{sufixo}"

    df = df.rename(columns=novo_nome)

    quantitativas_renomeadas = [
        f"{var}{sufixo}" for var in VARIAVEIS_YAML.quantitativas
        if f"{var}{sufixo}" in df.columns
    ]

    if quantitativas_renomeadas:
        df[quantitativas_renomeadas] = (
            df[quantitativas_renomeadas].fillna(0.0).astype(float)
        )

    return df
