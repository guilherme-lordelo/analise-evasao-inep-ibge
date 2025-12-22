from dataclasses import dataclass
from typing import Dict, List, Set, Optional


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
    remover_colunas: Optional[List[str]] = None

@dataclass(frozen=True)
class TabelaIBGEConfig:
    tabela_id: str
    descricao: str
    arquivo_xls: str

    sheets: List[SheetIBGEConfig]

_METODOS_MERGE_SUPORTADOS = {"soma", "media"}


def carregar_tabelas_ibge(_cfg: dict) -> Dict[str, TabelaIBGEConfig]:

	tabelas: Dict[str, TabelaIBGEConfig] = {}

	for tabela_id, info in _cfg.get("tabelas", {}).items():

		sheets: List[SheetIBGEConfig] = []

		for sheet in info.get("sheets", []):

			colunas_especificas: List[str] = sheet.get("colunas", [])
			remover_colunas: List[str] = sheet.get("remover_colunas", [])
			merges_cfg = sheet.get("merges_colunas", [])

			# Validação de remoção de colunas
			for col in remover_colunas:
				if col not in colunas_especificas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Coluna para remoção inexistente: '{col}'"
					)

			merges: List[MergeColunasConfig] = []
			destinos_usados: Set[str] = set()
			fontes_usadas: Set[str] = set()

			for idx, m in enumerate(merges_cfg):

				destino = m["destino"]
				fontes = m["fontes"]
				metodo = m.get("metodo", "soma")

				# Validações de merges
				if metodo not in _METODOS_MERGE_SUPORTADOS:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Método de merge não suportado: '{metodo}'"
					)

				if destino in colunas_especificas:
					raise ValueError(
						f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
						f"Destino de merge já existe como coluna: '{destino}'"
					)

				if destino in destinos_usados:
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

					if f in fontes_usadas:
						raise ValueError(
							f"[IBGE][{tabela_id}][{sheet['arquivo']}] "
							f"Coluna fonte '{f}' usada em mais de um merge"
						)

				destinos_usados.add(destino)
				fontes_usadas.update(fontes)

				merges.append(
					MergeColunasConfig(
						destino=destino,
						fontes=fontes,
						metodo=metodo
					)
				)

			sheets.append(
				SheetIBGEConfig(
					sheet_id=sheet.get("sheet_id"),
					descricao=sheet.get("descricao_sheet", ""),
					arquivo=sheet["arquivo"],
					colunas_especificas=colunas_especificas,
					merges_colunas=merges or None,
					remover_colunas=remover_colunas or None
				)
			)

		tabelas[tabela_id] = TabelaIBGEConfig(
			tabela_id=tabela_id,
			descricao=info.get("descricao_tabela", ""),
			arquivo_xls=f"{tabela_id}.xls",
			sheets=sheets
		)

	return tabelas