from brpipe.bridge.common.consumiveis import Consumivel

def exigir_temporalidade(item: Consumivel, nome_chart: str):
    if not getattr(item, "dim_temporal", False):
        raise ValueError(
            f"O consumível '{item.nome}' não possui dimensão temporal "
            f"e não pode ser usado em {nome_chart}."
        )
