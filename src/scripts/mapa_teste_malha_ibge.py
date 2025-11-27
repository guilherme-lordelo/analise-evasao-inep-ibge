import matplotlib.pyplot as plt
from viz.mapas.carregar_malhas import carregar_malha_municipios

def main():
    print("Carregando malha municipal IBGE...")
    gdf = carregar_malha_municipios()

    print("Gerando mapa básico...")
    gdf.plot(figsize=(12, 12))
    plt.title("Malha Municipal do Brasil – IBGE 2024")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
