from inep.config import VARIAVEIS_YAML, LIMPEZA


def limpar_municipios(df):
    comportamento = LIMPEZA.get("comportamento_sem_municipio", "descartar")
    padrao = LIMPEZA.get("valor_padrao_sem_municipio", {})

    # -----------------------------
    # Determinar cond_invalido
    # -----------------------------

     # Linhas onde o código do município é inválido

    COLUNA_COD_MUNICIPIO = VARIAVEIS_YAML.coluna_cod_municipio
    COLUNA_UF = VARIAVEIS_YAML.coluna_uf
    COLUNA_NOME_MUNICIPIO = VARIAVEIS_YAML.coluna_nome_municipio

    cond_invalido = (
        df[COLUNA_COD_MUNICIPIO].isna()
        | (df[COLUNA_COD_MUNICIPIO].astype(str).str.strip() == "")
        | (df[COLUNA_COD_MUNICIPIO].astype(str).str.strip() == "0")
    )

    # -----------------------------
    # Modo: descartar linhas inválidas
    # -----------------------------
    if comportamento == "descartar":
        return df[~cond_invalido]

    # -----------------------------
    # Modo: atribuir valores padrão
    # -----------------------------
    elif comportamento == "atribuir":
        df.loc[cond_invalido, COLUNA_COD_MUNICIPIO] = padrao.get(COLUNA_COD_MUNICIPIO, -1)

        # SG_UF é obrigatório e único
        df.loc[cond_invalido, COLUNA_UF] = padrao.get(COLUNA_UF, "ND")

        # Nome de município é OPCIONAL
        if COLUNA_NOME_MUNICIPIO is not None and COLUNA_NOME_MUNICIPIO in df.columns:
            df.loc[cond_invalido, COLUNA_NOME_MUNICIPIO] = padrao.get(
                COLUNA_NOME_MUNICIPIO, "SEM_MUNICIPIO"
            )

        return df

    # -----------------------------
    # Modo inválido
    # -----------------------------
    else:
        raise ValueError(f"Comportamento inválido para limpeza: {comportamento}")
