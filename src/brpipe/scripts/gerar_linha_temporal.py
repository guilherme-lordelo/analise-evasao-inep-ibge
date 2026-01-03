import pandas as pd
from brpipe.bridge.inep.bootstrap import CONTEXTO
from brpipe.utils.io import read_csv
from brpipe.viz.charts.linha_temporal.pipeline import executar_linha_temporal
from brpipe.utils.paths import arquivo_nacional

def main():
    VARIAVEIS = CONTEXTO.variaveis
    
    df = read_csv(arquivo_nacional)
    print(pd.api.types.is_numeric_dtype(df["NU_ANO_CENSO"]))
    min_year = df["NU_ANO_CENSO"].min()
    df_filtered = df[df["NU_ANO_CENSO"] > min_year]
    print("Renderizando gráficos de linha temporal...")
    executar_linha_temporal(df_filtered, variaveis=VARIAVEIS, coluna_ano=VARIAVEIS.coluna_ano)
    print("Renderização de charts concluída.")

if __name__ == "__main__":
    main()
