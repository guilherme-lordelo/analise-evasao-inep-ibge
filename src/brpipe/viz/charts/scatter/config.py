from dataclasses import dataclass
from typing import List, Optional
from brpipe.bridge.inep.tipos import ResultadoTipo
from brpipe.viz.charts.common import NormalizacaoPlot, PlotSpecBase
from brpipe.utils.config import load_config

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

@dataclass(frozen=True)
class ScatterConfig:
	plot: ScatterPlotConfig
	plots: List[ScatterPlotSpec]
	formato_saida: str
	dpi: int

def carregar_scatter(variaveis_inep) -> ScatterConfig:
	cfg = _CFG["scatter"]

	plot_cfg = cfg["plot"]

	plot = ScatterPlotConfig(
		figsize=tuple(plot_cfg["figsize"]),
		mostrar_titulo=plot_cfg["mostrar_titulo"],
		grid=plot_cfg["grid"],
	)

	plots = []

	for p in cfg["plots"]:

		territorio_chave = None
		territorio_valor = None

		if "territorio" in p:
			if len(p["territorio"]) != 1:
				raise ValueError(
					f"Plot '{p['nome']}' deve ter exatamente um território"
				)

			territorio_chave, territorio_valor = next(
				iter(p["territorio"].items())
			)

			if isinstance(territorio_valor, list):
				raise ValueError(
					f"Plot '{p['nome']}' não aceita múltiplos territórios"
				)

		var_x = variaveis_inep.get_variavel(p["eixo_x"])
		var_y = variaveis_inep.get_variavel(p["eixo_y"])

		resultados = {var_x.resultado, var_y.resultado}

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
				f"({var_x.resultado}, {var_y.resultado})"
			)

		plots.append(
			ScatterPlotSpec(
				nome=p["nome"],
				nivel=p["nivel"],
				eixo_x=p["eixo_x"],
				eixo_y=p["eixo_y"],
				territorio_chave=territorio_chave,
				territorio_valor=territorio_valor,
				normalizacao=normalizacao,
			)
		)

	return ScatterConfig(
		plot=plot,
		plots=plots,
		formato_saida=cfg["saida"]["formato"],
		dpi=cfg["saida"]["dpi"],
	)