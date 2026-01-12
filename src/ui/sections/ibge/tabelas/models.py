from enum import Enum
from dataclasses import dataclass, field
from uuid import uuid4

class FormaColuna(Enum):
	CRUA = "crua"
	SIMPLES = "simples"
	COMPLETA = "completa"


@dataclass
class ColunaEditavel:
	nome: str
	formato: str = "CONTAGEM"
	coluna_peso: str | None = None
	forma: FormaColuna = FormaColuna.CRUA
	uid: str = field(default_factory=lambda: uuid4().hex)