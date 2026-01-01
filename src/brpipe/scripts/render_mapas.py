from brpipe.viz.mapas.render.territorios import render_municipios, render_uf

def main():
    print("Renderizando mapas municipais...")
    render_municipios()

    print("Renderizando mapas por UF...")
    render_uf()

    print("Renderização concluída.")


if __name__ == "__main__":
    main()
