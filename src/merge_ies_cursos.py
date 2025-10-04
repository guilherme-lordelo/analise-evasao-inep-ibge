"""
src/merge_ies_cursos.py

Lê:
  data/processed/inep_reduzido.csv   (cursos reduzidos)
  data/processed/ies_reduzido.csv    (ies reduzido)

Faz merge por CO_IES (left join) e
salva (sobrescrevendo):
  data/processed/inep_ies_merged.csv

Também salva data/processed/missing_ies.csv se existirem cursos sem IES correspondente.
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]  # Project/
CURSOS_FILE = BASE_DIR / "data" / "processed" / "inep_reduzido.csv"
IES_FILE = BASE_DIR / "data" / "processed" / "ies_reduzido.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "inep_ies_merged.csv"
MISSING_FILE = BASE_DIR / "data" / "processed" / "missing_ies.csv"

def read_csv_fallback(path: Path):
    """Tenta ler com utf-8-sig, se falhar tenta latin1."""
    try:
        return pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig", low_memory=False)
    except Exception:
        return pd.read_csv(path, sep=";", dtype=str, encoding="latin1", low_memory=False)

def main():
    print(f"Carregando: {CURSOS_FILE}")
    cursos = read_csv_fallback(CURSOS_FILE)
    print(f"  -> cursos: {len(cursos):,} linhas")

    print(f"Carregando: {IES_FILE}")
    ies = read_csv_fallback(IES_FILE)
    print(f"  -> ies: {len(ies):,} linhas")

    # Normalize column names (remover espaços antes/depois)
    cursos.columns = cursos.columns.str.strip()
    ies.columns = ies.columns.str.strip()

    # Garantir que a chave CO_IES exista em ambas
    if "CO_IES" not in cursos.columns:
        raise KeyError(f"CO_IES não encontrada em {CURSOS_FILE}")
    if "CO_IES" not in ies.columns:
        raise KeyError(f"CO_IES não encontrada em {IES_FILE}")

    print("Fazendo merge (left join) por CO_IES...")
    merged = cursos.merge(ies, on="CO_IES", how="left", indicator=True)

    total_merged = len(merged)
    print(f"Total linhas após merge: {total_merged:,}")

    # Diagnóstico de correspondências perdidas
    missing = merged[merged["_merge"] == "left_only"]
    if not missing.empty:
        print(f"Atenção: {len(missing):,} cursos sem IES correspondente (salvando {MISSING_FILE.name})")
        missing.to_csv(MISSING_FILE, sep=";", index=False, encoding="utf-8-sig")
    else:
        # remover arquivo de missing anterior se existir
        if MISSING_FILE.exists():
            try:
                MISSING_FILE.unlink()
            except Exception:
                pass
        print("Todos os cursos encontraram IES correspondente.")

    # Remover sufixos _x (do lado cursos) e normalizar _y (do lado IES)
    cols_to_drop = [c for c in merged.columns if c.endswith("_x")]
    if cols_to_drop:
        print(f"Removendo {len(cols_to_drop)} colunas redundantes (sufixo _x).")
        merged = merged.drop(columns=cols_to_drop)

    # Renomear colunas com sufixo _y para remover o sufixo
    rename_map = {c: c[:-2] for c in merged.columns if c.endswith("_y")}
    if rename_map:
        merged = merged.rename(columns=rename_map)
        print(f"Renomeadas colunas: {list(rename_map.values())}")

    # Remover a coluna auxiliar do merge
    if "_merge" in merged.columns:
        merged = merged.drop(columns=["_merge"])

    # Salvar sobrescrevendo o arquivo merged
    merged.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8-sig")
    print(f"Merge concluído. Arquivo sobrescrito: {OUTPUT_FILE}")
    print(f"Shape final: {merged.shape}")

if __name__ == "__main__":
    main()
