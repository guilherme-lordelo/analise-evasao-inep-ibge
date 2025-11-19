import os
import sys
from utils.paths import DATA_RAW, DATA_INTERIM
from utils.io import write_csv
from inep.extracao.header import (
    ler_header,
    detectar_mapeamento,
    determinar_colunas_existentes,
    identificar_faltantes,
)
from inep.extracao.leitura_chunks import ler_em_chunks
from inep.extracao.limpeza import limpar_municipios
from inep.extracao.config import SEP, ENCODING


def executar_extracao():
    ano = input("Digite o ano do arquivo INEP a ser reduzido (ex: 2022): ").strip()
    input_filename = f"MICRODADOS_CADASTRO_CURSOS_{ano}.CSV"

    input_path = DATA_RAW / input_filename
    output_path = DATA_INTERIM / f"inep_reduzido_{ano}.csv"
    removidas_path = DATA_INTERIM / f"inep_removidas_{ano}.csv"

    if not input_path.exists():
        print(f"Arquivo não encontrado: {input_path}")
        print("Verifique se segue o padrão MICRODADOS_CADASTRO_CURSOS_XXXX.CSV.")
        sys.exit(1)

    os.makedirs(DATA_INTERIM, exist_ok=True)

    print(f" Lendo cabeçalho de {input_filename}...")
    header = ler_header(input_path)

    mapeamento = detectar_mapeamento(header)
    colunas_existentes = determinar_colunas_existentes(header, mapeamento)

    faltantes = identificar_faltantes(colunas_existentes, mapeamento)
    if faltantes:
        print(f"Atenção: colunas não encontradas: {faltantes}")

    print(f" Lendo arquivo completo de {ano} em chunks...")
    df = ler_em_chunks(input_path, colunas_existentes)
    df = df.rename(columns=mapeamento)

    print(" Limpando dados...")
    df_validos, df_invalidos = limpar_municipios(df)

    if len(df_invalidos) > 0:
        write_csv(df_invalidos, removidas_path, sep=SEP, encoding="utf-8")
        print(f" Linhas removidas salvas em: {removidas_path}")

    write_csv(df_validos, output_path, sep=SEP, encoding="utf-8")

    print(f" Arquivo reduzido salvo em: {output_path}")
    print(f" Total de linhas processadas: {len(df_validos):,}")


if __name__ == "__main__":
    executar_extracao()
