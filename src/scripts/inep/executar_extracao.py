# src/scripts/inep/executar_extracao.py

from utils.paths import RAW_INEP, INEP_REDUZIDO

from inep.extracao import orquestrar_extracao
from inep.checkpoints import salvar_checkpoint
from inep.config import (
	ANOS,
	ARQUIVOS_CONFIG,
)


def executar_extracao():
	print("EXTRAÇÃO INEP")
	print("Anos:", ANOS)

	for ano in ANOS:
		print(f"Extraindo INEP {ano}")

		try:
			input_filename = (
				f"{ARQUIVOS_CONFIG.extracao_prefixo_in}"
				f"{ano}"
				f"{ARQUIVOS_CONFIG.extracao_ext_in}"
			)

			output_filename = (
				f"{ARQUIVOS_CONFIG.extracao_prefixo_out}"
				f"{ano}"
				f"{ARQUIVOS_CONFIG.extracao_ext_out}"
			)

			input_path = RAW_INEP / input_filename
			output_path = INEP_REDUZIDO / output_filename

			if not input_path.exists():
				print(f"ERRO: Arquivo não encontrado: {input_path}")
				continue

			df = orquestrar_extracao(
				ano=ano,
				input_path=input_path,
			)

			print(f"Salvando arquivo reduzido em: {output_path}")
			salvar_checkpoint(
				df,
				output_path=output_path,
			)

			print(f"Total de linhas processadas: {len(df):,}")
			print()

		except Exception as e:
			print(f"[ERRO NO ANO {ano}]: {e}")
			continue


if __name__ == "__main__":
	executar_extracao()
