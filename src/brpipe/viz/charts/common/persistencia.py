# brpipe/viz/charts/persistencia.py
from pathlib import Path
import matplotlib.pyplot as plt

from brpipe.utils.paths import CHARTS_RENDER


def persistir_chart(
    *,
    fig: plt.Figure,
    tipo: str,
    nome: str,
    formato: str,
    dpi: int,
) -> None:
    """
    Persistência de charts.
    rendered/charts/<tipo>/<nome>.<formato>
    """

    out_dir: Path = CHARTS_RENDER / tipo
    out_dir.mkdir(parents=True, exist_ok=True)

    arquivo = out_dir / f"{nome}.{formato}"

    fig.savefig(
        arquivo,
        dpi=dpi,
        bbox_inches="tight",
    )
