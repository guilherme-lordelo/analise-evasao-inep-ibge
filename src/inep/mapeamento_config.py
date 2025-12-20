# src/inep/mapeamento_config.py

from dataclasses import dataclass

@dataclass(frozen=True)
class MapeamentoConfig:
	map_dict: dict[str, str]

	def detectar_mapeamento(
		self,
		header: list[str],
		variaveis_esperadas: list[str],
	) -> dict[str, str]:
		mapeamento = {}

		for esperado in variaveis_esperadas:
			if esperado in header:
				continue

			for alternativo, destino in self.map_dict.items():
				if destino == esperado and alternativo in header:
					mapeamento[alternativo] = esperado
					break

		return mapeamento

	def normalizar_coluna(self, coluna: str) -> str:
		"""
		Retorna o nome lógico da coluna (destino),
		ou a própria coluna se não houver mapeamento.
		"""
		return self.map_dict.get(coluna, coluna)

def carregar_mapeamento(cfg: dict) -> MapeamentoConfig:
	col_mappings = cfg.get("mapeamento_colunas", {})

	if not isinstance(col_mappings, dict):
		raise ValueError("mapeamento_colunas deve ser um dicionário")

	return MapeamentoConfig(map_dict=col_mappings)
