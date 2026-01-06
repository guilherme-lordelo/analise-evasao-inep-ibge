from dataclasses import dataclass
from typing import List, Optional
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.viz.charts.common import NormalizacaoPlot, PlotSpecBase
from brpipe.utils.config import load_config
from brpipe.viz.charts.common.consumiveis import Consumiveis
from brpipe.viz.charts.common.territorio import TerritoriosINEP

_CFG = load_config("charts")

@dataclass(frozen=True)
class ScatterPlotConfig:
	figsize: tuple[int, int]
	mostrar_titulo: bool
	grid: bool


@dataclass(frozen=True)
class ScatterPlotSpec(PlotSpecBase):
	eixo_x: str
	eixo_y: str
	territorio_chave: Optional[str] = None
	territorio_valor: Optional[str | int] = None
	normalizacao: NormalizacaoPlot = NormalizacaoPlot.COUNT

	@property
	def variaveis(self) -> list[str]:
		return [self.eixo_x, self.eixo_y]

@dataclass(frozen=True)
class ScatterConfig:
	plot: ScatterPlotConfig
	plots: List[ScatterPlotSpec]
	formato_saida: str
	dpi: int

def carregar_scatter(
    consumiveis: Consumiveis,
    territorios: TerritoriosINEP,
) -> ScatterConfig:
    cfg = _CFG["scatter"]

    plot_cfg = cfg["plot"]

    plot = ScatterPlotConfig(
        figsize=tuple(plot_cfg["figsize"]),
        mostrar_titulo=plot_cfg["mostrar_titulo"],
        grid=plot_cfg["grid"],
    )

    plots: list[ScatterPlotSpec] = []

    for p in cfg["plots"]:

        coluna_territorial = None
        valor_territorial = None

        if "territorio" in p:
            if len(p["territorio"]) != 1:
                raise ValueError(
                    f"Plot '{p['nome']}' deve ter exatamente um território"
                )

            (chave, valor_territorial), = p["territorio"].items()

            if isinstance(valor_territorial, list):
                raise ValueError(
                    f"Plot '{p['nome']}' não aceita múltiplos territórios"
                )

            coluna_territorial = territorios.coluna(
                nivel=p["nivel"],
                chave=chave,
            )

        item_x = consumiveis.get(p["eixo_x"])
        item_y = consumiveis.get(p["eixo_y"])

        resultados = {item_x.resultado, item_y.resultado}

        if resultados == {ResultadoTipo.COUNT}:
            normalizacao = NormalizacaoPlot.COUNT

        elif resultados.issubset({
            ResultadoTipo.LOGIT,
            ResultadoTipo.PROPORTION,
            ResultadoTipo.PERCENT_0_100,
        }):
            normalizacao = NormalizacaoPlot.RATIO

        else:
            raise ValueError(
                f"Plot '{p['nome']}' mistura tipos incompatíveis "
                f"({resultados})"
            )

        plots.append(
            ScatterPlotSpec(
                nome=p["nome"],
                nivel=p["nivel"],
                eixo_x=p["eixo_x"],
                eixo_y=p["eixo_y"],
                coluna_territorial=coluna_territorial,
                valor_territorial=valor_territorial,
                normalizacao=normalizacao,
            )
        )

    return ScatterConfig(
        plot=plot,
        plots=plots,
        formato_saida=cfg["saida"]["formato"],
        dpi=cfg["saida"]["dpi"],
    )
