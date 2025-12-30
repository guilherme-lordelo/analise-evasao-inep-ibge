from brpipe.viz.mapas.render.municipios import render_municipios_por_ano
from brpipe.viz.mapas.render.uf import render_uf_por_ano


def main():
    print("Renderizando mapas municipais...")
    render_municipios_por_ano()

    print("Renderizando mapas por UF...")
    render_uf_por_ano()

    print("Renderização concluída.")


if __name__ == "__main__":
    main()
