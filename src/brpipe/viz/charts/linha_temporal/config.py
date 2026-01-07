from dataclasses import dataclass
from typing import List
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.utils.config import load_config
from brpipe.viz.charts.common import NormalizacaoPlot, PlotSpecBase, Consumiveis, TerritoriosINEP

_CFG = load_config("charts")

@dataclass(frozen=True)
class LinhaTemporalPlotConfig:
    figsize: tuple[int, int]
    mostrar_titulo: bool
    grid: bool
    max_variaveis_por_plot: int

@dataclass(frozen=True)
class LinhaTemporalPlotSpec(PlotSpecBase):
    _variaveis: list[str]
    normalizacao: NormalizacaoPlot = NormalizacaoPlot.COUNT

    @property
    def variaveis(self) -> list[str]:
        return self._variaveis


@dataclass(frozen=True)
class LinhaTemporalConfig:
    plot: LinhaTemporalPlotConfig
    plots: List[LinhaTemporalPlotSpec]
    formato_saida: str
    dpi: int


def carregar_linha_temporal(
	consumiveis: Consumiveis,
	territorios: TerritoriosINEP,
) -> LinhaTemporalConfig:
	cfg = _CFG["linha_temporal"]

	plot_cfg = cfg["plot"]

	plot = LinhaTemporalPlotConfig(
		figsize=tuple(plot_cfg["figsize"]),
		mostrar_titulo=plot_cfg["mostrar_titulo"],
		grid=plot_cfg["grid"],
		max_variaveis_por_plot=plot_cfg["max_variaveis_por_plot"],
	)

	plots = []

	for p in cfg["plots"]:
		nomes_vars = p["variaveis"]

		if len(nomes_vars) > plot.max_variaveis_por_plot:
			raise ValueError(
				f"Plot '{p['nome']}' excede max_variaveis_por_plot"
			)

		coluna_territorial = None
		valor_territorial = None

		if "territorio" in p:
			(chave, valor_territorial), = p["territorio"].items()

			coluna_territorial = territorios.coluna(
				nivel=p["nivel"],
				chave=chave,
			)

		resultados = {
			consumiveis.get(nome).resultado
			for nome in nomes_vars
		}

		if resultados == {ResultadoTipo.COUNT}:
			normalizacao = NormalizacaoPlot.COUNT
		elif resultados.issubset({
			ResultadoTipo.LOGIT,
			ResultadoTipo.PROPORCAO,
			ResultadoTipo.PERCENT_0_100,
		}):
			normalizacao = NormalizacaoPlot.RATIO
		else:
			raise ValueError(
				f"Plot '{p['nome']}' mistura tipos incompatíveis" + f" ({resultados})"
			)

		plots.append(
			LinhaTemporalPlotSpec(
				nome=p["nome"],
				nivel=p["nivel"],
				_variaveis=nomes_vars,
				coluna_territorial=coluna_territorial,
				valor_territorial=valor_territorial,
				normalizacao=normalizacao,
			)
		)

	return LinhaTemporalConfig(
		plot=plot,
		plots=plots,
		formato_saida=cfg["saida"]["formato"],
		dpi=cfg["saida"]["dpi"],
	)
