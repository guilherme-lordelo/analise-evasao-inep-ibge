# src/scripts/inep/executar_evasao.py

from inep.evasao.pipeline import calcular_evasao
from inep.config import PARES


def executar_evasao():
    print("=== Iniciando processamento de evasão INEP ===\n")

    for par in PARES:
        ano_base, ano_seguinte = map(int, par.split("_"))
        print(f"Processando evasão para {ano_base} -> {ano_seguinte}...")

        try:
            calcular_evasao(ano_base, ano_seguinte)
            print(f"Concluído: {ano_base}_{ano_seguinte}\n")

        except Exception as e:
            print(f"\nERRO ao processar o par {ano_base}_{ano_seguinte}:")
            print(e)
            print("-" * 60 + "\n")

    print("=== Processamento de evasão finalizado ===")


if __name__ == "__main__":
    executar_evasao()
