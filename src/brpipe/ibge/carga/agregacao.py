import pandas as pd
from brpipe.ibge.carga.persistencia import persistir_tabela_final
from brpipe.ibge.config.models import AgregacaoColuna, SheetIBGEConfig
from brpipe.ibge.config.tipos import TipoAgregacao
from brpipe.utils.colunas_base import COL_NACIONAL, get_colunas_municipio
from brpipe.utils.iterador import iterar_sheets_ibge

def coletar_agregacoes_merges(
	tabela,
	sheet: SheetIBGEConfig,
) -> tuple[list[AgregacaoColuna], list[str]] | None:

	if not sheet.merges_colunas:
		return None

	agregacoes: list[AgregacaoColuna] = []
	fontes_remover: list[str] = []

	for merge in sheet.merges_colunas:
		col = merge.coluna

		if col.tipo_agregacao:
			agregacoes.append(
				AgregacaoColuna(
					nome=merge.destino,
					tipo=col.tipo_agregacao,
					coluna_peso=(
						merge.coluna_peso
						or col.coluna_peso
					),
				)
			)

		fontes_remover.extend(merge.fontes)

	return agregacoes, fontes_remover


def coletar_agregacoes(tabela, sheet: SheetIBGEConfig) -> list[AgregacaoColuna]:
	resultado = []

	for col in sheet.colunas_especificas:
		if col.tipo_agregacao:
			resultado.append(
				AgregacaoColuna(
					nome=col.nome,
					tipo=col.tipo_agregacao,
					coluna_peso=col.coluna_peso,
				)
			)

	return resultado or None

def soma_numerica(df: pd.DataFrame, coluna: str) -> float:
	valores = pd.to_numeric(df[coluna], errors="coerce")
	return valores.sum()

def media_ponderada(
	df: pd.DataFrame,
	coluna: str,
	peso: str,
) -> float:
	valores = pd.to_numeric(df[coluna], errors="coerce")
	pesos = pd.to_numeric(df[peso], errors="coerce")

	mask = valores.notna() & pesos.notna() & (pesos > 0)
	valores_f = valores[mask]
	pesos_f = pesos[mask]

	if valores_f.empty:
		return float("nan")

	total_peso = pesos_f.sum()
	if total_peso == 0:
		return float("nan")

	return (valores_f * pesos_f).sum() / total_peso

def agregar_estadual(
	df: pd.DataFrame,
	agregacoes: list[AgregacaoColuna],
) -> pd.DataFrame:

	registros = []
	UF = get_colunas_municipio()[1]

	for uf, g in df.groupby(UF):
		row = {UF: uf}

		for agg in agregacoes:
			if agg.nome not in g.columns:
				continue

			if agg.tipo == TipoAgregacao.SOMA:
				row[agg.nome] = soma_numerica(g, agg.nome)

			elif agg.tipo == TipoAgregacao.MEDIA_PONDERADA:
				if not agg.coluna_peso or agg.coluna_peso not in g.columns:
					continue

				row[agg.nome] = media_ponderada(
					g,
					coluna=agg.nome,
					peso=agg.coluna_peso,
				)

		registros.append(row)

	return pd.DataFrame(registros)

def agregar_nacional(
	df: pd.DataFrame,
	agregacoes: list[AgregacaoColuna],
) -> pd.DataFrame:

	row = {
		COL_NACIONAL: "BRASIL",
	}

	for agg in agregacoes:
		if agg.nome not in df.columns:
			continue

		if agg.tipo == TipoAgregacao.SOMA:
			row[agg.nome] = soma_numerica(df, agg.nome)

		elif agg.tipo == TipoAgregacao.MEDIA_PONDERADA:
			if not agg.coluna_peso or agg.coluna_peso not in df.columns:
				continue

			row[agg.nome] = media_ponderada(
				df,
				coluna=agg.nome,
				peso=agg.coluna_peso,
			)

	return pd.DataFrame([row])

def executar_agregacoes(
	df_municipal: pd.DataFrame,
	config_ibge: dict,
) -> None:

	agregacoes_raw = iterar_sheets_ibge(
		tabelas=config_ibge,
		fn=coletar_agregacoes,
	)

	agregacoes: list[AgregacaoColuna] = []
	if agregacoes_raw:
		agregacoes.extend(
			agg
			for sub in agregacoes_raw
			for agg in sub
		)

	merges_raw = iterar_sheets_ibge(
		tabelas=config_ibge,
		fn=coletar_agregacoes_merges,
	)

	fontes_remover: set[str] = set()

	if merges_raw:
		for aggs_merge, fontes in merges_raw:
			agregacoes.extend(aggs_merge)
			fontes_remover.update(fontes)

	colunas_drop = [
		c for c in fontes_remover
		if c in df_municipal.columns
	]

	if colunas_drop:
		df_municipal = df_municipal.drop(columns=colunas_drop)

	# Municipal
	persistir_tabela_final(df_municipal, nivel="municipal")

	# Estadual
	df_estadual = agregar_estadual(df_municipal, agregacoes)
	persistir_tabela_final(df_estadual, nivel="estadual")

	# Nacional
	df_nacional = agregar_nacional(df_municipal, agregacoes)
	persistir_tabela_final(df_nacional, nivel="nacional")
