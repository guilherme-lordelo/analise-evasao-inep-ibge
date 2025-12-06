from utils.paths import RAW_INEP, INTERIM_INEP
from utils.io import write_csv
from inep.extracao.header import (
    ler_header,
    detectar_mapeamento,
    determinar_colunas_existentes,
    identificar_faltantes,
)
from inep.extracao.leitura_chunks import ler_em_chunks
from inep.extracao.limpeza import limpar_municipios
from inep.config import (
    EXTRACAO_PREFIXO_IN,
    EXTRACAO_EXT_IN,
    EXTRACAO_PREFIXO_OUT,
    EXTRACAO_EXT_OUT,
    ANOS,
)


def processar_ano(ano: int):
    print("=" * 60)
    print(f"== Extraindo INEP {ano} ==")
    print("=" * 60)

    input_filename  = f"{EXTRACAO_PREFIXO_IN}{ano}{EXTRACAO_EXT_IN}"
    output_filename = f"{EXTRACAO_PREFIXO_OUT}{ano}{EXTRACAO_EXT_OUT}"

    input_path  = RAW_INEP / input_filename
    output_path = INTERIM_INEP / output_filename

    if not input_path.exists():
        print(f"ERRO: Arquivo não encontrado: {input_path}")
        return

    print(f"Lendo cabeçalho de {input_filename}...")
    header = ler_header(input_path)

    mapeamento = detectar_mapeamento(header)
    colunas_existentes = determinar_colunas_existentes(header, mapeamento)

    faltantes = identificar_faltantes(colunas_existentes, mapeamento)
    if faltantes:
        print(f"Atenção: colunas não encontradas: {faltantes}")

    print(f"Lendo arquivo de {ano} em chunks...")
    df = ler_em_chunks(input_path, colunas_existentes)

    df = df.rename(columns=mapeamento)

    print("Aplicando limpeza de municípios...")
    df = limpar_municipios(df)

    print(f"Salvando arquivo reduzido em: {output_path}")
    write_csv(df, output_path)

    print(f"Total de linhas processadas: {len(df):,}")
    print()


def executar_extracao():
    print("EXTRAÇÃO INEP")
    print("Anos:", ANOS)

    for ano in ANOS:
        try:
            processar_ano(ano)
        except Exception as e:
            print(f"[ERRO NO ANO {ano}]: {e}")
            continue


if __name__ == "__main__":
    executar_extracao()
