from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo, resolver_tipo_variavel_ibge
from brpipe.ibge.config.models import SheetIBGEConfig, TabelaIBGEConfig
from brpipe.viz.charts.common.consumiveis import Consumivel


class VariavelIBGE:
    def __init__(
        self,
        nome: str,
        resultado: ResultadoTipo,
        coluna: str,
    ):
        self.nome = nome.upper()
        self.coluna = coluna
        self.resultado = resultado

    def aplicar_formato(self, series: Series):
        return self.resultado.apply(series)

class VariaveisIBGE:
	def __init__(
		self,
		tabelas_cfg: dict[str, TabelaIBGEConfig],
		arquivo_final: str,
		tipo_default: ResultadoTipo,
	):
		self._arquivo_final = arquivo_final
		self._map = {}

		for tabela in tabelas_cfg.values():
			for sheet in tabela.sheets:
				self._registrar_sheet(sheet, tipo_default, tabela.tabela_id)

	def _registrar_sheet(self, sheet: SheetIBGEConfig, tipo_default: ResultadoTipo, tabela_id: str):
		ctx_base = f"[IBGE][{tabela_id}][{sheet.arquivo}]"

		for col in sheet.colunas_especificas:
			tipo = resolver_tipo_variavel_ibge(
				tipo_coluna=None,
				transformacao=None,
				tipo_default=tipo_default,
				ctx=f"{ctx_base}[{col}]",
			)

			self._map[col.upper()] = VariavelIBGE(
				nome=col,
				coluna=col,
				resultado=tipo,
			)

		if sheet.merges_colunas:
			for merge in sheet.merges_colunas:
				tipo = resolver_tipo_variavel_ibge(
					tipo_coluna=None,
					transformacao=None,
					tipo_default=tipo_default,
					ctx=f"{ctx_base}[MERGE:{merge.destino}]",
				)

				self._map[merge.destino.upper()] = VariavelIBGE(
					nome=merge.destino,
					coluna=merge.destino,
					resultado=tipo,
				)

		if sheet.transformacoes_colunas:
			for t in sheet.transformacoes_colunas:
				tipo = resolver_tipo_variavel_ibge(
					tipo_coluna=None,
					transformacao=t,
					tipo_default=tipo_default,
					ctx=f"{ctx_base}[TRANSF:{t.destino}]",
				)

				self._map[t.destino.upper()] = VariavelIBGE(
					nome=t.destino,
					coluna=t.destino,
					resultado=tipo,
				)

	def resolver(self, nome: str) -> Consumivel:
		chave = nome.upper()
		if chave not in self._map:
			raise KeyError(f"Variável IBGE '{nome}' não definida")
		return self._map[chave]

	def listar(self) -> list[str]:
		return list(self._map.keys())