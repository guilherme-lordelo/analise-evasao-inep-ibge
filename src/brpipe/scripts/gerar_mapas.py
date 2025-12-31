import sys

from brpipe.viz.mapas.plot.municipios import mapa_evasao_municipios
from brpipe.viz.mapas.plotly.uf import mapa_evasao_uf_plotly

def print_help():
    print("""
Uso:
    python gerar_mapas.py <tipo> [uf]

Tipos disponíveis:
    municipios           - Mapa municipal estático (ano fixo)
    uf                   - Mapa interativo por UF (Plotly + slider)
    municipios_uf <UF>   - Mapa municipal estático de uma UF

Exemplos:
    python gerar_mapas.py municipios
    python gerar_mapas.py uf
    python gerar_mapas.py municipios_uf BA
    """.strip())


def main():
    args = sys.argv[1:]

    if not args:
        print("Nenhum parâmetro informado.")
        print_help()
        return

    tipo = args[0].lower()

    ANO: int = 2021

    if tipo == "municipios":
        if not len(args) < 2:
            mapa_evasao_municipios(formula_indice=args[1], ano=ANO)
        else:
            mapa_evasao_municipios(formula_indice=0, ano=ANO)
    elif tipo == "uf":
        if not len(args) < 2:
            mapa_evasao_uf_plotly(formula_indice = args[1])
        else:
            mapa_evasao_uf_plotly(formula_indice = 0)

    elif tipo == "municipios_uf":
        if len(args) < 2:
            print("Erro: é necessário informar a sigla da UF.")
            print("Ex: python gerar_mapas.py municipios_uf BA")
            return

        sigla_uf = args[1].upper()
        mapa_evasao_municipios(sigla_uf=sigla_uf, ano=ANO)

    else:
        print(f"Tipo desconhecido: {tipo}")
        print_help()


if __name__ == "__main__":
    main()
