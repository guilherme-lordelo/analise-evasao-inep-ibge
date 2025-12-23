from dataclasses import dataclass
from typing import Dict, List, Set, Optional

@dataclass(frozen=True)
class TransformacaoColunaConfig:
    fonte: str                 # coluna original (ex: PERC_HOMEM)
    destino: str               # novo nome (ex: SEXO_LOGIT)
    tipo: str
    escala_origem: Optional[str] = None

@dataclass(frozen=True)
class MergeColunasConfig:
    destino: str
    fontes: List[str]
    metodo: str  # "soma", "media", etc.


@dataclass(frozen=True)
class SheetIBGEConfig:
    sheet_id: Optional[str]
    descricao: str
    arquivo: str

    colunas_especificas: List[str]

    merges_colunas: Optional[List[MergeColunasConfig]] = None
    transformacoes_colunas: Optional[List[TransformacaoColunaConfig]] = None
    remover_colunas: Optional[List[str]] = None

@dataclass(frozen=True)
class TabelaIBGEConfig:
    tabela_id: str
    descricao: str
    arquivo_xls: str

    sheets: List[SheetIBGEConfig]

_METODOS_MERGE_SUPORTADOS = {"soma", "media"}


_METODOS_TRANSFORMACAO_SUPORTADOS = {"logit"}


def carregar_tabelas_ibge(_cfg: dict) -> Dict[str, TabelaIBGEConfig]:

	tabelas: Dict[str, TabelaIBGEConfig] = {}
	sheet_count = 0

	for tabela_id, info in _cfg.get("tabelas", {}).items():

		sheets: List[SheetIBGEConfig] = []

		for sheet in info.get("sheets", []):
			sheet_count += 1

			colunas_especificas: List[str] = sheet.get("colunas", [])
			remover_colunas: List[str] = sheet.get("remover_colunas", [])
			merges_cfg = sheet.get("merges_colunas", [])
			transformacoes_colunas_cfg = sheet.get("transformacoes_colunas", [])

			for col in remover_colunas:
				if col not in colunas_especificas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Coluna para remoção inexistente: '{col}'"
					)

			merges: List[MergeColunasConfig] = []
			transformacoes: List[TransformacaoColunaConfig] = []

			destinos_merge: Set[str] = set()
			destinos_transformacao: Set[str] = set()
			fontes_merge: Set[str] = set()
			fontes_transformacao: Set[str] = set()

			for m in merges_cfg:

				destino = m["destino"]
				fontes = m["fontes"]
				metodo = m.get("metodo", "soma")

				if destino in colunas_especificas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de merge já existe como coluna: '{destino}'"
					)

				if destino in destinos_merge:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de merge duplicado: '{destino}'"
					)

				if len(fontes) < 2:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Merge '{destino}' deve ter ao menos 2 colunas fonte"
					)

				for f in fontes:
					if f not in colunas_especificas:
						raise ValueError(
							f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
							f"Coluna fonte inexistente no merge '{destino}': '{f}'"
						)

					if f in remover_colunas:
						raise ValueError(
							f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
							f"Coluna fonte '{f}' do merge '{destino}' "
							f"não pode ser removida"
						)

					if f in fontes_merge:
						raise ValueError(
							f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
							f"Coluna fonte '{f}' usada em mais de um merge"
						)

				destinos_merge.add(destino)
				fontes_merge.update(fontes)

				merges.append(
					MergeColunasConfig(
						destino=destino,
						fontes=fontes,
						metodo=metodo,
					)
				)

			colunas_disponiveis = (
				set(colunas_especificas)
				| destinos_merge
			)

			for t in transformacoes_colunas_cfg:

				fonte = t["fonte"]
				destino = t["destino"]
				tipo = t["tipo"]
				escala = t.get("escala_origem")

				if tipo not in _METODOS_TRANSFORMACAO_SUPORTADOS:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Tipo de transformação não suportado: '{tipo}'"
					)

				if fonte not in colunas_disponiveis:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Coluna fonte da transformação inexistente: '{fonte}'"
					)

				if fonte in remover_colunas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Coluna fonte '{fonte}' da transformação "
						f"não pode ser removida"
					)

				if destino in colunas_especificas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de transformação já existe como coluna: '{destino}'"
					)

				if destino in destinos_merge:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de transformação conflita com destino de merge: '{destino}'"
					)

				if destino in destinos_transformacao:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de transformação duplicado: '{destino}'"
					)

				destinos_transformacao.add(destino)
				fontes_transformacao.add(fonte)

				transformacoes.append(
					TransformacaoColunaConfig(
						fonte=fonte,
						destino=destino,
						tipo=tipo,
						escala_origem=escala,
					)
				)

			sheets.append(
				SheetIBGEConfig(
					sheet_id=sheet.get("sheet_id"),
					descricao=sheet.get("descricao_sheet", ""),
					arquivo=sheet["arquivo"],
					colunas_especificas=colunas_especificas,
					merges_colunas=merges or None,
					transformacoes_colunas=transformacoes or None,
					remover_colunas=remover_colunas or None,
				)
			)

		tabelas[tabela_id] = TabelaIBGEConfig(
			tabela_id=tabela_id,
			descricao=info.get("descricao_tabela", ""),
			arquivo_xls=f"{tabela_id}.xls",
			sheets=sheets,
		)

	print(f"Encontradas {len(tabelas)} tabelas e {sheet_count} sheets IBGE na configuração.")
	return tabelas

	return tabelas