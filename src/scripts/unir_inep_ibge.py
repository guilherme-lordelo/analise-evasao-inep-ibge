from utils.paths import DATA_PROCESSED
from utils.io import read_csv, write_csv
from utils.config import load_config
from ibge.carregamento.carregar_tabelas_finais import ler_tabelas_ibge
import pandas as pd

BASE_DIR = DATA_PROCESSED

# ----------------------------------
# 1. LER CONFIG DO INEP
# ----------------------------------
cfg_inep = load_config("inep")  # carrega inep.yml

pares = cfg_inep.get("pares", [])
anos_cfg = cfg_inep.get("anos", {})

ano_ini = anos_cfg.get("inicio")
ano_fim = anos_cfg.get("fim")

range_str = f"{ano_ini}_{ano_fim}"

ultimo_par = pares[-1]  # ex: "2023_2024"

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
write_csv(final_validos,
          BASE_DIR / f"municipios_evasao_valida_ibge_{range_str}.csv",
          sep=";")

write_csv(final_invalidos,
          BASE_DIR / f"municipios_evasao_invalida_ibge_{range_str}.csv",
          sep=";")

print(f"Merge com IBGE concluído para {range_str}")
