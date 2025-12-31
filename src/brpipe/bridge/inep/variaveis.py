from brpipe.inep.config.variaveis import VariaveisConfig


class VariaveisParaMapas:
    def __init__(self, cfg: VariaveisConfig):
        self._cfg = cfg

    @property
    def coluna_ano(self) -> str:
        return self._cfg.coluna_ano

    @property
    def territoriais(self) -> dict:
        return {
            "municipio": self._cfg.coluna_cod_municipio,
            "uf": self._cfg.coluna_uf,
        }

    def is_quantitativa(self, nome: str) -> bool:
        return nome in self._cfg.quantitativas
