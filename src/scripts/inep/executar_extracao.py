import sys
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


def executar_extracao():
    ano = input("Digite o ano do arquivo INEP a ser reduzido (ex: 2022): ").strip()
    input_filename = f"MICRODADOS_CADASTRO_CURSOS_{ano}.CSV"

    input_path = RAW_INEP / input_filename
    output_path = INTERIM_INEP / f"inep_reduzido_{ano}.csv"

    if not input_path.exists():
        print(f"Arquivo não encontrado: {input_path}")
        sys.exit(1)

    print(f"Lendo cabeçalho de {input_filename}...")
    header = ler_header(input_path)

    # ----------------------
    # Detecta colunas e mapeamentos
    # ----------------------
    mapeamento = detectar_mapeamento(header)
    colunas_existentes = determinar_colunas_existentes(header, mapeamento)

    faltantes = identificar_faltantes(colunas_existentes, mapeamento)
    if faltantes:
        print(f"Atenção: colunas não encontradas: {faltantes}")

    # ----------------------
    # Leitura em chunks
    # ----------------------
    print(f"Lendo arquivo completo de {ano} em chunks...")
    df = ler_em_chunks(input_path, colunas_existentes)

    # Aplica renomeação conforme mapeamento
    df = df.rename(columns=mapeamento)

    # ----------------------
    # Limpeza de municípios
    # ----------------------
    print("Aplicando limpeza de municípios...")
    df = limpar_municipios(df)

    # ----------------------
    # Escrita do CSV reduzido (intermediário)
    # ----------------------
    print(f"Salvando arquivo reduzido em: {output_path}")
    write_csv(df, output_path)

    print(f"Total de linhas processadas: {len(df):,}")


if __name__ == "__main__":
    executar_extracao()
