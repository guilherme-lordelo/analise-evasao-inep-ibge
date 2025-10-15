# Projeto - Integração e Visualização de Dados do INEP e IBGE: um Pipeline para Análise da Evasão no Ensino Superior

Este projeto tem como objetivo analisar a evasão na educação superior brasileira, a partir dos microdados do Censo da Educação Superior (INEP, 2024), relacionando-os com indicadores socioeconômicos municipais (IBGE).

## Estrutura de Diretórios

- `data/raw/` → dados brutos originais do INEP, não modificados (não versionados no GitHub)
- `data/interim/` → dados parcialmente processados do INEP
- `data/interim/ibge_csv/` → dados IBGE extraídos de XLS e convertidos para CSV
- `data/processed/` → dados finais do INEP
- `data/processed/ibge_csv_final/` → tabelas IBGE finais
- `src/` → scripts de processamento

## Scripts Principais

- **INEP**
  - `src/extract_inep.py` → gera datasets reduzidos (`inep_reduzido_YYYY.csv`) em `data/interim/`
  - `src/extract_ies.py` → gera dataset de instituições (`inep_ies_reduzido.csv`)
  - `src/merge_ies_cursos.py` → consolida cursos e IES em `inep_ies_merged.csv`

- **IBGE**
  - `src/extract_ibge.py` → extrai planilhas XLS e gera CSVs intermediários em `data/interim/ibge_csv/`
  - `src/ibge_limpar_tabelas.py` → limpa e padroniza colunas conforme `src/ibge_colunas.py`, salvando tabelas finais em `data/processed/ibge_csv_final/`

- **Agregação**
  - `src/aggregate_two_years.py` → agrega dois anos consecutivos de microdados do INEP, gerando dataset consolidado em `data/processed/` com cálculo da taxa de evasão por município


## Fluxo de Processamento

1. **INEP**
   1. Colocar os arquivos brutos do INEP em `data/raw/`.
   2. Executar `src/extract_inep.py` para gerar datasets reduzidos em `data/interim/` (ex: `inep_reduzido_2022.csv`).
   3. Executar `src/extract_ies.py` para gerar dataset de instituições (`inep_ies_reduzido.csv`).
   4. Executar `src/merge_ies_cursos.py` para consolidar cursos e IES em `inep_ies_merged.csv`.

2. **IBGE**
   1. Colocar os arquivos XLS do IBGE em `data/raw/ibge_xls/`.
   2. Executar `src/extract_ibge.py` para extrair os sheets e gerar CSVs intermediários em `data/interim/ibge_csv/`.
   3. Executar `src/ibge_limpar_tabelas.py` para limpar e padronizar colunas conforme `src/ibge_colunas.py`, salvando os arquivos finais em `data/processed/ibge_csv_final/`.

3. **Integração e Análise**
   1. Executar `src/aggregate_two_years.py` para agregar dois anos consecutivos de microdados do INEP, gerando dataset consolidado em `data/processed/` com cálculo da taxa de evasão por município.
   2. (Próximo passo) Harmonizar e integrar as bases do IBGE com os dados do INEP para análises exploratórias e modelagem.

## Requisitos

- Python 3.11+
- Pandas
- Numpy

Instalar dependências:

```bash
pip install -r requirements.txt

