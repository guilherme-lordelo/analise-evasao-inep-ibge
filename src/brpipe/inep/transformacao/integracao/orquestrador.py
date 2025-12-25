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

from brpipe.inep.config.transformacao import INEPConfigTransformacao


def orquestrar_integracao(
    config: INEPConfigTransformacao,
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

    leitores = config.leitores_por_ano

    # WIDE
    if formato == "wide":

        cat_results = fetch_categoricas_wide(
            leitores_por_ano=leitores,
            colunas_quantitativas=config.colunas_quantitativas,
            include_estadual=include_estadual,
            include_nacional=include_nacional,
        )

        df_quant_all = preparar_quantitativas_wide(
            leitores_por_ano=leitores,
            colunas_categoricas=config.colunas_categoricas,
        )

        return merge_wide(
            df_quant_all=df_quant_all,
            cat_mun=cat_results["municipal"],
            cat_est=cat_results["estadual"],
            cat_nat=cat_results["nacional"],
        )

    # LONG
    else:
        cat_results = fetch_categoricas_long(
            leitores_por_ano=leitores,
            colunas_quantitativas=config.colunas_quantitativas,
            include_estadual=include_estadual,
            include_nacional=include_nacional,
        )

        df_quant_all = preparar_quantitativas_long(
            leitores_por_ano=leitores,
            colunas_categoricas=config.colunas_categoricas,
            colunas_quantitativas=config.colunas_quantitativas,
        )

        return merge_long(
            df_quant_all=df_quant_all,
            cat_mun=cat_results["municipal"],
            cat_est=cat_results["estadual"],
            cat_nat=cat_results["nacional"],
        )
