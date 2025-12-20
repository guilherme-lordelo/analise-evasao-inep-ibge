# src/inep/io_config.py

from dataclasses import dataclass


@dataclass(frozen=True)
class IOConfig:
	# Extração
	encoding_in: str = "latin1"
	sep_in: str = ";"
	chunksize: int = 100_000

	# Saída
	encoding_out: str = "utf-8"
	sep_out: str = ";"
	compress: bool = False
	ordem_colunas: list[str] | None = None

	def __post_init__(self):
		if not isinstance(self.chunksize, int) or self.chunksize <= 0:
			raise ValueError("chunksize deve ser inteiro positivo")

def carregar_io(cfg: dict) -> IOConfig:
	extracao = cfg.get("extracao", {})
	saida = cfg.get("saida", {})

	return IOConfig(
		encoding_in=extracao.get("encoding", "latin1"),
		sep_in=extracao.get("sep", ";"),
		chunksize=extracao.get("chunksize", 100_000),

		encoding_out=saida.get("encoding", "utf-8"),
		sep_out=saida.get("sep", ";"),
		compress=saida.get("compress", None),
		ordem_colunas=saida.get("ordem_colunas")
	)
