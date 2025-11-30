from inep.config import LIMPEZA_CFG

def limpar_municipios(df):
    comportamento = LIMPEZA_CFG.get("comportamento_sem_municipio", "descartar")
    padrao = LIMPEZA_CFG.get("valor_padrao_sem_municipio", {})

    cond_invalido = (
        df["CO_MUNICIPIO"].isna()
        | (df["CO_MUNICIPIO"].astype(str).str.strip() == "")
        | (df["CO_MUNICIPIO"].astype(str).str.strip() == "0")
    )

    if comportamento == "descartar":
        return df[~cond_invalido]

    elif comportamento == "atribuir":
        df.loc[cond_invalido, "CO_MUNICIPIO"] = padrao.get("CO_MUNICIPIO", -1)
        df.loc[cond_invalido, "SG_UF"] = padrao.get("SG_UF", "ND")
        df.loc[cond_invalido, "NO_MUNICIPIO"] = padrao.get("NO_MUNICIPIO", "SEM_MUNICIPIO")
        return df

    else:
        raise ValueError(f"Comportamento inválido para limpeza: {comportamento}")
