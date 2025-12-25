from dataclasses import dataclass
from typing import Dict, List, Set

from brpipe.utils.colunas_base import get_colunas_municipio


@dataclass(frozen=True)
class VariaveisConfig:

    variaveis_cfg: dict

    campos_padrao: List[str]

    coluna_cod_municipio: str
    coluna_uf: str
    coluna_nome_municipio: str | None

    variaveis: List[str]

    temporais: List[str]
    categoricas_original: List[str]
    categoricas: List[str]
    quantitativas: List[str]

    valores_categoricos: Dict[str, Set[str]]

    coluna_ano: str
    coluna_peso: str


def carregar_variaveis(_cfg: dict) -> VariaveisConfig:

    variaveis_cfg = _cfg.get("variaveis", {})

    campos_padrao = get_colunas_municipio()

    if not (2 <= len(campos_padrao) <= 3):
        raise ValueError(
            "CAMPOS_PADRAO deve conter no mínimo 2 e no máximo 3 campos "
            "(cod_municipio, uf [, nome_municipio])"
        )

    coluna_cod_municipio = campos_padrao[0]
    coluna_uf = campos_padrao[1]
    coluna_nome_municipio = campos_padrao[2] if len(campos_padrao) == 3 else None

    temporais = list(variaveis_cfg.get("temporais", {}).keys())
    categoricas = list(variaveis_cfg.get("categoricas", {}).keys())
    quantitativas = list(variaveis_cfg.get("quantitativas", {}).keys())

    if len(temporais) != 1:
        raise ValueError(
            f"Deve haver apenas uma variável de ano, "
            f"encontradas: {temporais}"
        )

    coluna_ano = temporais[0]

    variaveis: List[str] = []
    variaveis.extend(campos_padrao)

    for categoria, campos in variaveis_cfg.items():
        variaveis.extend(campos.keys())

    variaveis = list(dict.fromkeys(variaveis))

    valores_categoricos: Dict[str, Set[str]] = {}
    categoricas_original: List[str] = []

    for var, props in variaveis_cfg.get("categoricas", {}).items():
        valores = set(props.get("valores", {}).keys())
        filtro_excluir = set(props.get("filtro_excluir", []))

        if filtro_excluir:
            categoricas_original.append(var)

        valores_filtrados = valores - filtro_excluir

        if not valores_filtrados:
            raise ValueError(
                f"A variável categórica '{var}' ficou sem valores possíveis "
                f"após aplicação do filtro_excluir={filtro_excluir}"
            )

        valores_categoricos[var] = valores_filtrados


    coluna_peso = _cfg.get("coluna_peso_inep", "QT_MAT_TOTAL")

    if coluna_ano not in variaveis:
        raise ValueError(
            f"Variável temporal '{coluna_ano}' não está presente em VARIAVEIS"
        )

    if coluna_peso not in variaveis:
        raise ValueError(
            f"Coluna de peso '{coluna_peso}' não está presente em VARIAVEIS"
        )

    return VariaveisConfig(
        variaveis_cfg=variaveis_cfg,
        campos_padrao=campos_padrao,
        coluna_cod_municipio=coluna_cod_municipio,
        coluna_uf=coluna_uf,
        coluna_nome_municipio=coluna_nome_municipio,
        variaveis=variaveis,
        temporais=temporais,
        categoricas=categoricas,
        categoricas_original=categoricas_original,
        quantitativas=quantitativas,
        valores_categoricos=valores_categoricos,
        coluna_ano=coluna_ano,
        coluna_peso=coluna_peso
    )
