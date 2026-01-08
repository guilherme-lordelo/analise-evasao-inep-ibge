from brpipe.ibge.transformacao import transformar_ibge
from brpipe.ibge.carga import carregar_ibge

if __name__ == "__main__":
	sheets = transformar_ibge()

	if sheets:
		print("Iniciando camada LOAD do IBGE...")
		print(f"Sheets transformados: {len(sheets)}")
		carregar_ibge(sheets)
	else:
		print("Nenhum dado transformado para carregar.")
