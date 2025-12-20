# src/inep/arquivos_config.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ArquivosConfig:
	extracao_prefixo_in: str
	extracao_ext_in: str
	extracao_prefixo_out: str
	extracao_ext_out: str

	transformacao_prefixo_out: str
	transformacao_ext_out: str
	transformacao_niveis: list[str]

	def __post_init__(self):
		if not self.transformacao_niveis:
			raise ValueError("transformacao_niveis não pode ser vazio")

		if len(set(self.transformacao_niveis)) != len(self.transformacao_niveis):
			raise ValueError("transformacao_niveis contém valores duplicados")

def carregar_arquivos(cfg: dict) -> ArquivosConfig:
    arq_cfg = cfg.get("arquivos", {})

    extracao_cfg = arq_cfg.get("extracao", {})
    transformacao_cfg = arq_cfg.get("transformacao", {})

    return ArquivosConfig(
        extracao_prefixo_in=extracao_cfg["prefixo_input"],
        extracao_ext_in=extracao_cfg["extensao_input"],
        extracao_prefixo_out=extracao_cfg["prefixo_output"],
        extracao_ext_out=extracao_cfg["extensao_output"],

        transformacao_prefixo_out=transformacao_cfg["prefixo_output"],
        transformacao_ext_out=transformacao_cfg["extensao_output"],
        transformacao_niveis=transformacao_cfg.get(
			"niveis", ["municipios", "estados", "nacional"])
    )