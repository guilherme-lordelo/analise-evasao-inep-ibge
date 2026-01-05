from brpipe.bridge.inep import CONTEXTO
from brpipe.viz.charts.scatter.pipeline import executar_scatter


def main():
	VARIAVEIS = CONTEXTO.variaveis
	METRICAS = CONTEXTO.metricas

	print("Renderizando gráficos scatter...")
	executar_scatter(variaveis=VARIAVEIS, metricas=METRICAS, coluna_ano=VARIAVEIS.coluna_ano)
	print("Renderização de charts concluída.")


if __name__ == "__main__":
	main()
