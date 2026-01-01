from dataclasses import dataclass
from typing import Callable

import pandas as pd

from brpipe.inep.checkpoints import carregar_checkpoint
from brpipe.inep.config import ANOS, ARQUIVOS, VARIAVEIS_YAML, FORMULAS_CONFIG
from brpipe.utils.paths import INEP_REDUZIDO


@dataclass(frozen=True)
class INEPConfigTransformacao:
    anos: list[int]

    colunas_categoricas: list[str]
    colunas_quantitativas: list[str]
    campos_padrao: list[str]
    coluna_ano: str | None

    formulas: dict
    limites_validacao: dict

    leitores_por_ano: dict[int, Callable[[], pd.DataFrame]]


def construir_config_transformacao() -> INEPConfigTransformacao:
    anos = list(ANOS)

    def leitor_ano(ano: int):
        return carregar_checkpoint(
            INEP_REDUZIDO
            / f"{ARQUIVOS.extracao_prefixo_out}{ano}{ARQUIVOS.extracao_ext_out}"
        )

    leitores = {
        ano: (lambda a=ano: leitor_ano(a))
        for ano in anos
    }

    return INEPConfigTransformacao(
        anos=anos,
        colunas_categoricas=VARIAVEIS_YAML.categoricas,
        colunas_quantitativas=VARIAVEIS_YAML.quantitativas,
        campos_padrao=VARIAVEIS_YAML.campos_padrao,
        coluna_ano=VARIAVEIS_YAML.coluna_ano,
        formulas=FORMULAS_CONFIG.formulas,
        limites_validacao=FORMULAS_CONFIG.limites_validacao,
        leitores_por_ano=leitores,
    )
