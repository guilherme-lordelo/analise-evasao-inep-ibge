from inep.evasao.pipeline import calcular_evasao

def main():
    ano_base = input("Digite o ANO BASE (ex: 2022): ").strip()
    ano_seguinte = input("Digite o ANO SEGUINTE (ex: 2023): ").strip()

    try:
        calcular_evasao(ano_base, ano_seguinte)
    except Exception as e:
        print("\nERRO DURANTE O PROCESSAMENTO:")
        print(e)

if __name__ == "__main__":
    main()
