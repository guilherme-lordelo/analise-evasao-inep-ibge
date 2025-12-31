from brpipe.bridge.inep import CONTEXTO

VARIAVEIS = CONTEXTO.variaveis
_lista_formulas = CONTEXTO.formulas.listar_metricas()
FORMULAS = [item.upper() for item in _lista_formulas]
