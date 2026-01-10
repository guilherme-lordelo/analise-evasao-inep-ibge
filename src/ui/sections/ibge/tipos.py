from typing import TypedDict, Optional


class ColunaPesoDef(TypedDict):
	nome_logico: str
	coluna_fisica: str


class ColunaNormalizada(TypedDict):
	nome: str
	formato: str
	coluna_peso: Optional[str]
