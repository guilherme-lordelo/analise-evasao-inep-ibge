from brpipe.ibge.transformacao import transformar_ibge
from brpipe.ibge.carga import carregar_ibge

if __name__ == "__main__":
	dfs_transformados = transformar_ibge()
	if dfs_transformados:
		print("Iniciando camada LOAD do IBGE...")
		print(f"Sheets transformados: {len(dfs_transformados)}")
		carregar_ibge(dfs_transformados)
	else:
		print("Nenhum dado transformado para carregar.")
	