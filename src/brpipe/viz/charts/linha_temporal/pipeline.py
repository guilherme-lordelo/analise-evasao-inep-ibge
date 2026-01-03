from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.config import LINHA_TEMPORAL
from brpipe.viz.charts.linha_temporal.render import render_linha_temporal


def executar_linha_temporal(
    df,
    variaveis: VariaveisINEP,
    coluna_ano: str,
):
    print(LINHA_TEMPORAL.variaveis)
    for nome in LINHA_TEMPORAL.variaveis:

        if not variaveis.is_quantitativa(nome):
            continue
        print(nome)
        render_linha_temporal(
            df=df,
            variaveis=variaveis,
            coluna_ano=coluna_ano,
            nome_variavel=nome,
            cfg=LINHA_TEMPORAL,
        )
