from inep.config import LIMPEZA_CFG, COLUNA_COD_MUNICIPIO, COLUNA_UF, COLUNA_NOME_MUNICIPIO


def limpar_municipios(df):
    comportamento = LIMPEZA_CFG.get("comportamento_sem_municipio", "descartar")
    padrao = LIMPEZA_CFG.get("valor_padrao_sem_municipio", {})

    # -----------------------------
    # Determinar cond_invalido
    # -----------------------------

     # Linhas onde o código do município é inválido

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
