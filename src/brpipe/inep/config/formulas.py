# src/inep/formulas_config.py

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class FormulaConfig:
	"""
	Representa uma fórmula configurável do INEP.
	"""
	nome: str
	descricao: str
	expressao: str
	formato: str
	regras_validacao: List[str]


@dataclass(frozen=True)
class FormulasConfig:
	"""
	Container das fórmulas e seus limites de validação.
	"""
	formulas: Dict[str, FormulaConfig]
	limites_validacao: dict


def _validar_expressao_basica(nome: str, expressao: str):
	if not isinstance(expressao, str) or not expressao.strip():
		raise ValueError(
			f"Fórmula '{nome}' deve possuir uma expressão não vazia"
		)

	if "{p}" not in expressao or "{n}" not in expressao:
		raise ValueError(
			f"Fórmula '{nome}' deve conter os placeholders '{{p}}' e '{{n}}'"
		)


def carregar_formulas(_cfg: dict) -> FormulasConfig:
	formulas_cfg = _cfg.get("formulas", {})
	limites_validacao = _cfg.get("validacao_limites", {})

	formulas: Dict[str, FormulaConfig] = {}

	for nome, info in formulas_cfg.items():
		expressao = info.get("expressao")
		descricao = info.get("descricao", "")
		formato = info.get("formato", "")
		regras = info.get("validacao", {}).get("regras", [])

		_validar_expressao_basica(nome, expressao)

		if not isinstance(regras, list):
			raise ValueError(
				f"Regras de validação da fórmula '{nome}' devem ser uma lista"
			)

		formulas[nome] = FormulaConfig(
			nome=nome,
			descricao=descricao,
			expressao=expressao,
			formato=formato,
			regras_validacao=regras,
		)

	return FormulasConfig(
		formulas=formulas,
		limites_validacao=limites_validacao,
	)
