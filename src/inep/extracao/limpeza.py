def limpar_municipios(df):
    invalidos = df[
        df["CO_MUNICIPIO"].isna()
        | (df["CO_MUNICIPIO"].astype(str).str.strip() == "")
        | (df["CO_MUNICIPIO"].astype(str).str.strip() == "0")
    ]

    df_validos = df[
        df["CO_MUNICIPIO"].notna()
        & (df["CO_MUNICIPIO"].astype(str).str.strip() != "")
        & (df["CO_MUNICIPIO"].astype(str).str.strip() != "0")
    ]

    return df_validos, invalidos
