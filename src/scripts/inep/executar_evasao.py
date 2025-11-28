from inep.evasao.pipeline import calcular_evasao

def main():
    ano_seguinte_str = input("Digite o ano de referência (ex: 2023): ").strip()

    try:
        ano_seguinte = int(ano_seguinte_str)
    except ValueError:
        print("Ano inválido. Digite apenas números, ex: 2023.")
        return

    ano_base = ano_seguinte - 1

    print(f"Processando evasão para {ano_base} → {ano_seguinte}...")

    try:
        calcular_evasao(ano_base, ano_seguinte)
    except Exception as e:
        print("\nERRO DURANTE O PROCESSAMENTO:")
        print(e)

if __name__ == "__main__":
    main()
