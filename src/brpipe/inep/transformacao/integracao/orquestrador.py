from brpipe.inep.config import (
    ANOS,
    ARQUIVOS,
    VARIAVEIS_YAML,
)
from brpipe.utils.paths import INEP_REDUZIDO
from brpipe.utils.io import read_csv

from brpipe.inep.transformacao.integracao.wide.pipeline import (
    fetch_categoricas as fetch_categoricas_wide,
    preparar_quantitativas as preparar_quantitativas_wide,
)
from brpipe.inep.transformacao.integracao.wide.agregacao import (
    merge_quantitativas_com_categoricas as merge_wide
)

from brpipe.inep.transformacao.integracao.long.pipeline import (
    fetch_categoricas as fetch_categoricas_long,
    preparar_quantitativas as preparar_quantitativas_long,
)
from brpipe.inep.transformacao.integracao.long.agregacao import (
    merge_quantitativas_com_categoricas as merge_long
)

def _construir_leitores_csv(
    anos: list[str],
):
    """
    Constrói leitores CSV por ano (agnóstico de formato).
    """

    def leitor_ano(ano: str):
        return read_csv(
            INEP_REDUZIDO
            / f"{ARQUIVOS.extracao_prefixo_out}{ano}{ARQUIVOS.extracao_ext_out}"
        )

    return {
        ano: (lambda a=ano: leitor_ano(a))
        for ano in anos
    }



def orquestrar_integracao(
    formato: str = "long",
    include_estadual: bool = True,
    include_nacional: bool = True,
):
    """
    Executa a agregação no formato WIDE ou LONG.
    """

    formato = formato.lower()
    if formato not in {"wide", "long"}:
        raise ValueError("formato deve ser 'wide' ou 'long'")

    anos = [str(ano) for ano in ANOS]

    # WIDE
    if formato == "wide":

        leitores = _construir_leitores_csv(anos)

        cat_results = fetch_categoricas_wide(
            leitores_por_ano=leitores,
            colunas_quantitativas=VARIAVEIS_YAML.quantitativas,
            include_estadual=include_estadual,
            include_nacional=include_nacional,
        )

        df_quant_all = preparar_quantitativas_wide(
            leitores_por_ano=leitores,
            colunas_categoricas=VARIAVEIS_YAML.categoricas,
        )

        return merge_wide(
            df_quant_all=df_quant_all,
            cat_mun=cat_results["municipal"],
            cat_est=cat_results["estadual"],
            cat_nat=cat_results["nacional"],
        )

    # LONG
    else:
        leitores = _construir_leitores_csv(anos)

        cat_results = fetch_categoricas_long(
            leitores_por_ano=leitores,
            colunas_quantitativas=VARIAVEIS_YAML.quantitativas,
            include_estadual=include_estadual,
            include_nacional=include_nacional,
        )

        df_quant_all = preparar_quantitativas_long(
            leitores_por_ano=leitores,
            colunas_categoricas=VARIAVEIS_YAML.categoricas,
            colunas_quantitativas=VARIAVEIS_YAML.quantitativas,
        )

        return merge_long(
            df_quant_all=df_quant_all,
            cat_mun=cat_results["municipal"],
            cat_est=cat_results["estadual"],
            cat_nat=cat_results["nacional"],
        )
