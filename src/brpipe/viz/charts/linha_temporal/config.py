from dataclasses import dataclass
from typing import List, Optional
from brpipe.bridge.inep.tipos import ResultadoTipo
from brpipe.utils.config import load_config
from brpipe.viz.charts.common import NormalizacaoPlot, PlotSpecBase


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
	territorio_chave: Optional[str] = None
	territorio_valor: Optional[str | int] = None
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



def carregar_linha_temporal(variaveis_inep) -> LinhaTemporalConfig:
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

		resultados = set()
		for nome in nomes_vars:
			var = variaveis_inep.get_variavel(nome)
			resultados.add(var.resultado)

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
				f"Plot '{p['nome']}' mistura tipos incompatíveis"
			)

		plots.append(
			LinhaTemporalPlotSpec(
				nome=p["nome"],
				nivel=p["nivel"],
				_variaveis=nomes_vars,
				territorio_chave=territorio_chave,
				territorio_valor=territorio_valor,
				normalizacao=normalizacao,
			)
		)

	return LinhaTemporalConfig(
		plot=plot,
		plots=plots,
		formato_saida=cfg["saida"]["formato"],
		dpi=cfg["saida"]["dpi"],
	)
