import sys

from brpipe.viz.mapas.plot.municipios import mapa_evasao_municipios
from brpipe.viz.mapas.plot.uf import mapa_evasao_uf


def print_help():
    print("""
Uso:
    python gerar_mapas.py <tipo> [uf]

Tipos disponíveis:
    municipios           - Mapa municipal do Brasil inteiro
    uf                   - Mapa agregado por estados (UF)
    municipios_uf <UF>   - Mapa municipal apenas de um estado

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

    if tipo == "municipios":
        mapa_evasao_municipios()

    elif tipo == "uf":
        mapa_evasao_uf()

    elif tipo == "municipios_uf":
        if len(args) < 2:
            print("Erro: é necessário informar a sigla da UF.")
            print("Ex: python gerar_mapas.py municipios_uf BA")
            return

        sigla_uf = args[1].upper()
        mapa_evasao_municipios(sigla_uf=sigla_uf)

    else:
        print(f"Tipo desconhecido: {tipo}")
        print_help()


if __name__ == "__main__":
    main()
