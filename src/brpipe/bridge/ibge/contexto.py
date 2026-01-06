from dataclasses import dataclass
from brpipe.bridge.ibge.variaveis import VariaveisIBGE


@dataclass(frozen=True)
class IbgeContext:
	variaveis: VariaveisIBGE