from brpipe.inep.config.formulas import FormulaConfig, FormulasConfig


class FormulasParaMetricas:
    def __init__(self, cfg: FormulasConfig):
        self._cfg = cfg

    def listar_metricas(self) -> list[str]:
        _lista_formulas = list(self._cfg.formulas.keys())
        return [item.upper() for item in _lista_formulas]

    def resolver(self, nome: str) -> FormulaConfig:
        if nome not in self._cfg.formulas:
            raise KeyError(f"Métrica '{nome}' não definida no INEP")
        return self._cfg.formulas[nome]
