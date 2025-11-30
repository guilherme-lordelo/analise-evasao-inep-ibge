from inep.config import (
    LIMPEZA_CFG,
    CAMPO_COD_MUNICIPIO,
    CAMPO_UF,
    CAMPO_NOME_MUNICIPIO,
)


def limpar_municipios(df):
    comportamento = LIMPEZA_CFG.get("comportamento_sem_municipio", "descartar")
    padrao = LIMPEZA_CFG.get("valor_padrao_sem_municipio", {})

    # -----------------------------
    # Determinar cond_invalido
    # -----------------------------
    campo = CAMPO_COD_MUNICIPIO

    cond_invalido = (
        df[campo].isna()
        | (df[campo].astype(str).str.strip() == "")
        | (df[campo].astype(str).str.strip() == "0")
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
        df.loc[cond_invalido, campo] = padrao.get(campo, -1)

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
