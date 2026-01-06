from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo


class VariavelIBGE:
    def __init__(
        self,
        nome: str,
        resultado: ResultadoTipo,
        coluna: str,
    ):
        self.nome = nome.upper()
        self.coluna = coluna
        self.resultado = resultado

    def aplicar_formato(self, series: Series):
        return self.resultado.apply(series)

class VariaveisIBGE:
    def __init__(self, colunas: dict[str, ResultadoTipo]):
        self._map = {
            nome.upper(): VariavelIBGE(
                nome=nome,
                coluna=nome,
                resultado=resultado,
            )
            for nome, resultado in colunas.items()
        }

    def resolver(self, nome: str) -> VariavelIBGE:
        chave = nome.upper()
        if chave not in self._map:
            raise KeyError(f"Variável IBGE '{nome}' não definida")
        return self._map[chave]

    def listar(self) -> list[str]:
        return list(self._map.keys())
