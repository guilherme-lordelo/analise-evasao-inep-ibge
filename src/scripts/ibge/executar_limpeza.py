from ibge.config import COLUNAS_POR_TABELA
from ibge.limpeza.pipeline_limpeza import processar_varias_tabelas

def main():
    print("=== Processador de Tabelas IBGE ===\n")

    print("Tabelas disponíveis:")
    print(", ".join(COLUNAS_POR_TABELA.keys()))

    escolha = input(
        "\nDigite o nome das tabelas a processar (separadas por vírgula ou 'todas'): "
    ).strip()

    if escolha.lower() == "todas":
        arquivos = list(COLUNAS_POR_TABELA.keys())

    else:
        mapa_lower = {k.lower(): k for k in COLUNAS_POR_TABELA.keys()}
        arquivos = [
            mapa_lower[a.strip().lower()]
            for a in escolha.split(",")
            if a.strip().lower() in mapa_lower
        ]

    if not arquivos:
        print("Nenhum arquivo válido selecionado.")
        return

    processar_varias_tabelas(arquivos, COLUNAS_POR_TABELA)


if __name__ == "__main__":
    main()
