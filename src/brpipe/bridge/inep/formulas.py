from brpipe.inep.config.formulas import FormulaConfig, FormulasConfig


class FormulasParaMetricas:
    def __init__(self, cfg: FormulasConfig):
        self._cfg = cfg

    def listar_metricas(self) -> list[str]:
        return list(self._cfg.formulas.keys())

    def resolver(self, nome: str) -> FormulaConfig:
        if nome not in self._cfg.formulas:
            raise KeyError(f"Métrica '{nome}' não definida no INEP")
        return self._cfg.formulas[nome]
