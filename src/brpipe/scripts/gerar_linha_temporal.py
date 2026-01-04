import pandas as pd
from brpipe.bridge.inep import CONTEXTO
from brpipe.viz.charts.linha_temporal.pipeline import executar_linha_temporal

def main():
    VARIAVEIS = CONTEXTO.variaveis
    
    print("Renderizando gráficos de linha temporal...")
    executar_linha_temporal(variaveis=VARIAVEIS, coluna_ano=VARIAVEIS.coluna_ano)
    print("Renderização de charts concluída.")

if __name__ == "__main__":
    main()
