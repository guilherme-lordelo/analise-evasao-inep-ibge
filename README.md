# Projeto - Integração e Visualização de Dados do INEP e IBGE: um Pipeline para Análise da Evasão no Ensino Superior

Este projeto tem como objetivo analisar a evasão na educação superior brasileira, a partir dos microdados do Censo da Educação Superior (INEP, 2024), relacionando-os com indicadores socioeconômicos municipais (IBGE).

---

## Arquitetura e Estrutura de Diretórios

A estrutura de diretórios foi projetada para organizar o fluxo de dados (brutos, intermediários e processados) e os scripts de processamento.

### Diretórios de Dados

Os dados são armazenados na pasta `data/`, com a seguinte organização:

- `data/raw/` → Dados brutos originais (não versionados).
- `data/interim/` → Dados parcialmente processados e intermediários.
- `data/processed/` → Dados agregados e conjuntos de dados finais prontos para análise.

### Diretórios de Código-Fonte (`src/`)

O código-fonte é modularizado nos seguintes subdiretórios:

- `src/inep/` → Lógica de processamento dos dados do INEP.
- `src/ibge/` → Lógica de processamento dos dados do IBGE.
- `src/utils/` → Funções de apoio (leitura/escrita de arquivos, definição de caminhos).
- `src/scripts/` → *Entry points* (pontos de entrada) para executar os pipelines completos.

---

## Fluxo de Processamento

O processamento é dividido em duas pipelines principais (INEP e IBGE), que culminam em uma etapa de união final.

### 1. Pipeline INEP — Processamento e Evasão

Este pipeline foca na extração dos microdados do INEP e no cálculo das taxas de evasão.

- **Extração e Limpeza:** Módulos em `src/inep/extracao/` lidam com a leitura dos arquivos brutos, aplicação de filtros iniciais e limpeza dos dados, gerando arquivos intermediários em `data/interim/`.
- **Cálculo de Evasão:** Os módulos em `src/inep/evasao/` e `src/inep/pares/` orquestram o cálculo da evasão por pares de anos, validação de municípios, ponderação e agregação dos resultados por UF e Brasil.
- **Execução:** O script `src/scripts/inep/executar_evasao.py` coordena a execução de todo o fluxo.

### 2. Pipeline IBGE — Extração e Padronização

Este pipeline extrai e padroniza dados socioeconômicos do IBGE para enriquecer o conjunto de dados final.

- **Extração:** Módulos em `src/ibge/extracao/` convertem as planilhas XLS originais para o formato CSV.
- **Limpeza e Padronização:** Os scripts em `src/ibge/limpeza/` padronizam as colunas e os dados, gerando tabelas finais em `data/processed/ibge_csv_final/`.
- **Carregamento:** `src/ibge/carregamento/carregar_tabelas_finais.py` lê e consolida essas tabelas limpas.
- **Execução:** O script `src/scripts/ibge/executar_limpeza.py` coordena a execução deste fluxo.

### 3. União Final (Merge)

A etapa final une os resultados processados de ambos os pipelines:

- **União:** O script `src/scripts/unir_inep_ibge.py` carrega os dados processados do INEP e do IBGE, realiza a união das tabelas e gera os conjuntos de dados finais, como `municipios_evasao_valida_ibge_YYYY_YYYY.csv`, localizados em `data/processed/`.

---

## Scripts Principais

Os *entry points* para a execução dos pipelines estão localizados em `src/scripts/`:

- `src/scripts/inep/executar_extracao.py`: Inicia a extração e limpeza inicial do INEP.
- `src/scripts/inep/executar_evasao.py`: Executa o cálculo completo da evasão do INEP.
- `src/scripts/ibge/executar_limpeza.py`: Executa o processamento completo dos dados IBGE.
- `src/scripts/unir_inep_ibge.py`: Realiza a união final dos dados processados.

## Etapas do Processamento

1. **INEP**  
   1. Colocar os arquivos brutos do INEP em `data/raw/`.  
   2. Executar `src\scripts\inep\executar_extracao.py` para gerar datasets reduzidos em `data/interim/` (ex: `inep_reduzido_2022.csv`).  
   3. Executar `src\scripts\inep\executar_evasao.py` para unir pares de anos consecutivos e calcular a evasão anual (`evasao_YYYY_YYYY.csv`), salvando em `data/processed/`.  
   4. Executar `src\scripts\inep\executar_uniao_pares.py` para combinar todos os pares de anos de evasão (`evasao_YYYY_YYYY.csv`), calcular médias e evasões acumuladas ponderadas, e gerar arquivos agregados por município, UF e Brasil em `data/processed/`.

2. **IBGE**  
   1. Colocar os arquivos XLS do IBGE em `data/raw/ibge_xls/`.  
   2. Executar `src\scripts\ibge\executar_extracao.py` para extrair as planilhas e gerar CSVs intermediários em `data/interim/ibge_csv/`.  
   3. Executar `src\scripts\ibge\executar_limpeza.py` para limpar e padronizar colunas conforme `src/ibge_colunas.py`, salvando as tabelas finais em `data/processed/ibge_csv_final/`.  

3. **União das bases INEP e IBGE**  
   1. Executar `src\scripts\unir_inep_ibge.py` para integrar os resultados agregados de evasão com os dados censitários do IBGE (`ibge_csv_final/`), produzindo versões finais completas (`municipios_evasao_valida_ibge_2020_2024.csv` e `municipios_evasao_invalida_ibge_2020_2024.csv`) em `data/processed/`.  


## Requisitos

- Python 3.11+
functools==0.5
numpy==2.3.4
pandas==2.3.3

Instalar dependências:

```bash
pip install -r requirements.txt

