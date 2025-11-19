# src/ibge/columns.py

# -------------------------------------------------------------
# DICIONÁRIO DE COLUNAS POR ARQUIVO
# -------------------------------------------------------------

COLUNAS_POR_TABELA = {
    # -------------------------------------------------
    # Tabela 1 - População total, urbana/rural e sexo
    # -------------------------------------------------
    "tab1.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_TOTAL", "PERC_URBANA", "PERC_RURAL",
        "PERC_HOMEM", "PERC_MULHER", "RAZAO_SEXO"
    ],

    # -------------------------------------------------
    # Tabela 2 - População residente por faixas etárias
    #   A = Total, B = Urbana, C = Rural
    # -------------------------------------------------
    "tab2A.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_TOTAL",
        "PERC_0_A_5", "PERC_6_A_14",
        "PERC_15_A_24", "PERC_25_A_39",
        "PERC_40_A_59", "PERC_60_OU_MAIS"
    ],

    "tab2B.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_URBANA",
        "PERC_0_A_5_URBANA", "PERC_6_A_14_URBANA",
        "PERC_15_A_24_URBANA", "PERC_25_A_39_URBANA",
        "PERC_40_A_59_URBANA", "PERC_60_OU_MAIS_URBANA"
    ],

    "tab2C.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_RURAL",
        "PERC_0_A_5_RURAL", "PERC_6_A_14_RURAL",
        "PERC_15_A_24_RURAL", "PERC_25_A_39_RURAL",
        "PERC_40_A_59_RURAL", "PERC_60_OU_MAIS_RURAL"
    ],

    # -------------------------------------------------
    # Tabela 3 - Pessoas de 15 anos ou mais, por faixa etária
    # -------------------------------------------------
    "tab3A.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "PESSOAS_15_MAIS_TOTAL", "PERC_15_MAIS",
        "PESSOAS_15_24_TOTAL", "PERC_15_24",
        "PESSOAS_25_39_TOTAL", "PERC_25_39",
        "PESSOAS_40_59_TOTAL", "PERC_40_59",
        "PESSOAS_60_MAIS_TOTAL", "PERC_60_MAIS"
    ],

    # -------------------------------------------------
    # Tabela 4 - Unidades domésticas por sexo do responsável
    # -------------------------------------------------
    "tab4.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "UNIDADES_DOMESTICAS_TOTAL", "PERC_UNICO_RESP", "PERC_MAIS_DE_1_RESP",
        "UNIDADES_DOMESTICAS_HOMEM", "PERC_UNICO_RESP_HOMEM", "PERC_MAIS_DE_1_RESP_HOMEM",
        "UNIDADES_DOMESTICAS_MULHER", "PERC_UNICO_RESP_MULHER", "PERC_MAIS_DE_1_RESP_MULHER"
    ],

    # -------------------------------------------------
    # Tabela 7 - Domicílios particulares permanentes por tipo de saneamento
    #   A = Total, B = Urbana, C = Rural
    # -------------------------------------------------
    "tab7A.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "DOMICILIOS_TOTAL",
        "PERC_SANEAMENTO_ADEQUADO", "PERC_SANEAMENTO_SEMI_ADEQUADO", "PERC_SANEAMENTO_INADEQUADO"
    ],
    "tab7B.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "DOMICILIOS_URBANOS",
        "PERC_SANEAMENTO_ADEQUADO_URBANO", "PERC_SANEAMENTO_SEMI_ADEQUADO_URBANO", "PERC_SANEAMENTO_INADEQUADO_URBANO"
    ],
    "tab7C.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "DOMICILIOS_RURAIS",
        "PERC_SANEAMENTO_ADEQUADO_RURAL", "PERC_SANEAMENTO_SEMI_ADEQUADO_RURAL", "PERC_SANEAMENTO_INADEQUADO_RURAL"
    ],

    # -------------------------------------------------
    # Tabela 8 - Rendimento domiciliar per capita nominal (médio e quartis)
    #   A = Total, B = Urbana, C = Rural
    # -------------------------------------------------
    "tab8A.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "VALOR_MEDIO_TOTAL",
        "QUARTIL_1_TOTAL", "QUARTIL_2_TOTAL", "QUARTIL_3_TOTAL"
    ],
    "tab8B.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "VALOR_MEDIO_URBANO",
        "QUARTIL_1_URBANO", "QUARTIL_2_URBANO", "QUARTIL_3_URBANO"
    ],
    "tab8C.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "VALOR_MEDIO_RURAL",
        "QUARTIL_1_RURAL", "QUARTIL_2_RURAL", "QUARTIL_3_RURAL"
    ],

    # -------------------------------------------------
    # Tabela 10 - Rendimento médio por cor ou raça (pessoas 10+)
    # -------------------------------------------------
    "tab10.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "VALOR_MEDIO_BRANCA", "VALOR_MEDIO_PRETA",
        "VALOR_MEDIO_PARDA", "VALOR_MEDIO_AMARELA", "VALOR_MEDIO_INDIGENA"
    ],

    # -------------------------------------------------
    # Tabela 12 - População residente por faixas de rendimento
    #   A = Total, B = Urbana, C = Rural
    # -------------------------------------------------
    "tab12A.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_TOTAL",
        "PERC_ATE_70_REAIS", "PERC_ATE_QUARTO_SM",
        "PERC_ATE_MEIO_SM", "PERC_ATE_60_PERC_MEDIANA"
    ],
    "tab12B.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_URBANA",
        "PERC_ATE_70_REAIS_URBANA", "PERC_ATE_QUARTO_SM_URBANA",
        "PERC_ATE_MEIO_SM_URBANA", "PERC_ATE_60_PERC_MEDIANA_URBANA"
    ],
    "tab12C.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_RESIDENTE_RURAL",
        "PERC_ATE_70_REAIS_RURAL", "PERC_ATE_QUARTO_SM_RURAL",
        "PERC_ATE_MEIO_SM_RURAL", "PERC_ATE_60_PERC_MEDIANA_RURAL"
    ],

    # -------------------------------------------------
    # Tabela 13 - População residente com saneamento inadequado e classes de rendimento
    # -------------------------------------------------
    "tab13.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "POP_SANEAMENTO_INADEQUADO_TOTAL",
        "PERC_ATE_70_REAIS", "PERC_ATE_QUARTO_SM",
        "PERC_ATE_MEIO_SM", "PERC_ATE_60_PERC_MEDIANA"
    ],

    # -------------------------------------------------
    # Tabela 14 - Taxa de analfabetismo da população de 15 anos ou mais
    # -------------------------------------------------
    "tab14.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "TX_ANALFABETISMO_2000_TOTAL", "TX_ANALFABETISMO_2010_TOTAL",
        "TX_ANALFABETISMO_2000_15_24", "TX_ANALFABETISMO_2010_15_24",
        "TX_ANALFABETISMO_2000_25_59", "TX_ANALFABETISMO_2010_25_59",
        "TX_ANALFABETISMO_2000_60_MAIS", "TX_ANALFABETISMO_2010_60_MAIS"
    ],

    # -------------------------------------------------
    # Tabela 16 - Proporção de crianças (0 a 5 anos) em domicílios vulneráveis
    # -------------------------------------------------
    "tab16.csv": [
        "CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO_OU_CLASSE",
        "PERC_RESPONSAVEL_ANALFABETO_2000", "PERC_RESPONSAVEL_ANALFABETO_2010",
        "PERC_SANEAMENTO_INADEQUADO_2000", "PERC_SANEAMENTO_INADEQUADO_2010",
        "PERC_AMBOS_ANALFABETO_E_INADEQUADO_2000", "PERC_AMBOS_ANALFABETO_E_INADEQUADO_2010"
    ],
}
