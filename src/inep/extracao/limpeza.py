from inep.config import LIMPEZA_CFG, get_campos_municipio


def limpar_municipios(df):
    comportamento = LIMPEZA_CFG.get("comportamento_sem_municipio", "descartar")
    padrao = LIMPEZA_CFG.get("valor_padrao_sem_municipio", {})

    # -----------------------------
    # Determinar cond_invalido
    # -----------------------------
    CAMPO_COD_MUNICIPIO = get_campos_municipio()[0]  # Código do município
    CAMPO_UF = get_campos_municipio()[1]  # Sigla da UF
    CAMPO_NOME_MUNICIPIO = (
        get_campos_municipio()[2] if len(get_campos_municipio()) > 2 else None
    )  # Nome do município (opcional)

     # Linhas onde o código do município é inválido

    cond_invalido = (
        df[CAMPO_COD_MUNICIPIO].isna()
        | (df[CAMPO_COD_MUNICIPIO].astype(str).str.strip() == "")
        | (df[CAMPO_COD_MUNICIPIO].astype(str).str.strip() == "0")
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
        df.loc[cond_invalido, CAMPO_COD_MUNICIPIO] = padrao.get(CAMPO_COD_MUNICIPIO, -1)

        # SG_UF é obrigatório e único
        df.loc[cond_invalido, CAMPO_UF] = padrao.get(CAMPO_UF, "ND")

        # Nome de município é OPCIONAL
        if CAMPO_NOME_MUNICIPIO is not None and CAMPO_NOME_MUNICIPIO in df.columns:
            df.loc[cond_invalido, CAMPO_NOME_MUNICIPIO] = padrao.get(
                CAMPO_NOME_MUNICIPIO, "SEM_MUNICIPIO"
            )

        return df

    # -----------------------------
    # Modo inválido
    # -----------------------------
    else:
        raise ValueError(f"Comportamento inválido para limpeza: {comportamento}")
