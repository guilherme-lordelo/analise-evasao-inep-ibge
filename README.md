# Projeto - Integração e Visualização de Dados do INEP e IBGE: um Pipeline para Análise da Evasão no Ensino Superior

Este projeto tem como objetivo analisar a evasão na educação superior brasileira, a partir dos microdados do Censo da Educação Superior (INEP, 2024), relacionando-os com indicadores socioeconômicos municipais (IBGE).

## Estrutura de Diretórios

- `data/raw/` → dados brutos originais do INEP, não modificados (não versionados no GitHub)
- `data/interim/` → dados parcialmente processados do INEP
- `data/interim/ibge_csv/` → dados IBGE extraídos de XLS e convertidos para CSV
- `data/processed/` → dados agregados finais
- `data/processed/ibge_csv_final/` → tabelas IBGE finais
- `src/` → scripts de processamento

## Scripts Principais

- **INEP**
  - `src/extract_inep.py` → gera datasets reduzidos (`inep_reduzido_YYYY.csv`) em `data/interim/`
  - `src/aggregate_two_years.py` → Une pares de anos e calcula evasão anual (`evasao_YYYY_YYYY.csv`) em `data/processed`

- **IBGE**
  - `src/extract_ibge.py` → extrai planilhas XLS e gera CSVs intermediários em `data/interim/ibge_csv/`
  - `src/ibge_limpar_tabelas.py` → limpa e padroniza colunas conforme `src/ibge_colunas.py`, salvando tabelas finais em `data/processed/ibge_csv_final/`

- **Agregação**  
  - `src/agregar_evasao.py` → combina todos os pares de anos de evasão (`evasao_YYYY_YYYY.csv`), calcula médias e evasões acumuladas ponderadas, e gera arquivos agregados por município, UF e Brasil em `data/processed/`  
  - `src/merge_ibge_evasao.py` → une os resultados agregados de evasão com os dados censitários do IBGE (`ibge_csv_final/`), produzindo versões finais completas (`municipios_evasao_valida_ibge_2020_2024.csv` e `municipios_evasao_invalida_ibge_2020_2024.csv`) em `data/processed/`



## Fluxo de Processamento

1. **INEP**  
   1. Colocar os arquivos brutos do INEP em `data/raw/`.  
   2. Executar `src/extract_inep.py` para gerar datasets reduzidos em `data/interim/` (ex: `inep_reduzido_2022.csv`).  
   3. Executar `src/aggregate_two_years.py` para unir pares de anos consecutivos e calcular a evasão anual (`evasao_YYYY_YYYY.csv`), salvando em `data/processed/`.  

2. **IBGE**  
   1. Colocar os arquivos XLS do IBGE em `data/raw/ibge_xls/`.  
   2. Executar `src/extract_ibge.py` para extrair as planilhas e gerar CSVs intermediários em `data/interim/ibge_csv/`.  
   3. Executar `src/ibge_limpar_tabelas.py` para limpar e padronizar colunas conforme `src/ibge_colunas.py`, salvando as tabelas finais em `data/processed/ibge_csv_final/`.  

3. **Agregação e Integração**  
   1. Executar `src/agregar_evasao.py` para combinar todos os pares de anos de evasão (`evasao_YYYY_YYYY.csv`), calcular médias e evasões acumuladas ponderadas, e gerar arquivos agregados por município, UF e Brasil em `data/processed/`.  
   2. Executar `src/merge_ibge_evasao.py` para integrar os resultados agregados de evasão com os dados censitários do IBGE (`ibge_csv_final/`), produzindo versões finais completas (`municipios_evasao_valida_ibge_2020_2024.csv` e `municipios_evasao_invalida_ibge_2020_2024.csv`) em `data/processed/`.  


## Requisitos

- Python 3.11+
functools==0.5
numpy==2.3.4
pandas==2.3.3

Instalar dependências:

```bash
pip install -r requirements.txt

