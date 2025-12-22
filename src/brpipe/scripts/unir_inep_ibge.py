from brpipe.utils.paths import DATA_PROCESSED
from brpipe.utils.io import read_csv, write_csv
from brpipe.utils.config import load_config
from brpipe.ibge.carga.carregar_tabelas_finais import ler_tabelas_ibge
from brpipe.inep.config import PARES, ANO_INICIO, ANO_FIM
import pandas as pd

BASE_DIR = DATA_PROCESSED

# ----------------------------------
# 1. LER CONFIG DO INEP
# ----------------------------------

range_str = f"{ANO_INICIO}_{ANO_FIM}"
ultimo_par = PARES[-1]

# ----------------------------------
# 2. LER EVASÃO CONSOLIDADA
# ----------------------------------
validos = read_csv(BASE_DIR / f"municipios_evasao_valida_{range_str}.csv", sep=";")
invalidos = read_csv(BASE_DIR / f"municipios_evasao_invalida_{range_str}.csv", sep=";")

# ----------------------------------
# 3. LER IBGE
# ----------------------------------
ibge_all = ler_tabelas_ibge()

# ----------------------------------
# 4. LER O "ULTIMO PAR" PARA TRAZER NOMES E UF
# ----------------------------------
ult_df = read_csv(BASE_DIR / f"evasao_{ultimo_par}.csv", sep=";")
info_df = ult_df[["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"]].drop_duplicates()

ibge_all = pd.merge(info_df, ibge_all, on="CO_MUNICIPIO", how="left")

# ----------------------------------
# 5. MERGES FINAIS
# ----------------------------------
final_validos = pd.merge(validos, ibge_all, on="CO_MUNICIPIO", how="left")
final_invalidos = pd.merge(invalidos, ibge_all, on="CO_MUNICIPIO", how="left")

# ----------------------------------
# 6. SALVAR
# ----------------------------------
write_csv(final_validos, BASE_DIR / f"municipios_evasao_valida_ibge_{range_str}.csv")

write_csv(final_invalidos, BASE_DIR / f"municipios_evasao_invalida_ibge_{range_str}.csv")

print(f"Merge com IBGE concluído para {range_str}")
