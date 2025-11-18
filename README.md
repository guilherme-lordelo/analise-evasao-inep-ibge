# Projeto - Integração e Visualização de Dados do INEP e IBGE: um Pipeline para Análise da Evasão no Ensino Superior

Este projeto tem como objetivo analisar a evasão na educação superior brasileira, a partir dos microdados do Censo da Educação Superior (INEP, 2024), relacionando-os com indicadores socioeconômicos municipais (IBGE).

## Estrutura de Diretórios

- `data/raw/` → dados brutos originais do INEP, não modificados (não versionados no GitHub)
- `data/interim/` → dados parcialmente processados do INEP
- `data/interim/ibge_csv/` → dados IBGE extraídos de XLS e convertidos para CSV
- `data/processed/` → dados agregados finais
- `data/processed/ibge_csv_final/` → tabelas IBGE finais
- `src/` → scripts de processamento


---

## 1. INEP — Processamento e Evasão

### Extração
- `src/inep/extracao.py`  
  Lê os dados brutos do INEP e gera versões reduzidas em `data/interim/`.

### Geração de pares de evasão
- `src/inep/gerar_evasao_por_pares.py`  
  Gera arquivos `evasao_YYYY_YYYY.csv` em `data/processed/`.

### Carregamento de pares
- `src/inep/carregamento_pares.py`
  - `ler_pares_evasao()` → lê todos os arquivos de evasão.  
  - `merge_pares()` → concatena os pares.

### Validação
- `src/inep/validacao.py`
  - `separar_validos_invalidos()` → separa municípios válidos e inválidos.

### Ponderação
- `src/inep/ponderacao.py`
  - `calcular_media_ponderada()` → calcula médias ponderadas.

### Agregação
- `src/inep/agregacao_evasao.py`
  - `agrega_evasao(df, coluna)` → agrega evasão por UF, BR ou outro grupo.

---

## 2. IBGE — Extração e Padronização

### Extração
- `src/ibge/extracao.py`  
  Converte planilhas XLS para CSV em `data/interim/ibge_csv/`.

### Limpeza
- `src/ibge/limpeza.py`  
  Padroniza colunas conforme `colunas.py`, gerando arquivos em  
  `data/processed/ibge_csv_final/`.

### Leitura das Tabelas Finais
- `src/ibge/leitura_tabelas_finais.py`
  - `ler_tabelas_ibge()` → lê e consolida todas as tabelas limpas.

---

## 3. Utils — Funções de Apoio

- `src/utils/io.py`  
  - `read_csv()`  
  - `write_csv()`  

- `src/utils/paths.py`  
  Define caminhos como:
  - `DATA_RAW`
  - `DATA_INTERIM`
  - `DATA_PROCESSED`

---

## 4. Merge — União Final INEP + IBGE

### União dos pares INEP (agregado)
- `src/merge/uniao_inep_pares.py`  
  Executa o pipeline:
  1. Lê e mescla os pares (`carregamento_pares`)
  2. Separa válidos / inválidos (`validacao`)
  3. Calcula médias ponderadas (`ponderacao`)
  4. Agrega por UF e Brasil (`agregacao_evasao`)
  5. Gera:
     - `municipios_evasao_valida_2020_2024.csv`
     - `municipios_evasao_invalida_2020_2024.csv`
     - `evasao_uf_e_brasil_2020_2024.csv`

### União final com IBGE
- `src/merge/uniao_inep_ibge.py`  
  Pipeline:
  1. Lê evasão válida e inválida
  2. Carrega tabelas IBGE consolidadas (`ler_tabelas_ibge`)
  3. Obtém informações atualizadas do último ano (`NO_MUNICIPIO`, `SG_UF`)
  4. Faz merge com IBGE
  5. Gera:
     - `municipios_evasao_valida_ibge_2020_2024.csv`
     - `municipios_evasao_invalida_ibge_2020_2024.csv`

---

## Fluxo de Processamento

1. **INEP**  
   1. Colocar os arquivos brutos do INEP em `data/raw/`.  
   2. Executar `src/inep/extracao.py` para gerar datasets reduzidos em `data/interim/` (ex: `inep_reduzido_2022.csv`).  
   3. Executar `src/inep/gerar_evasao_por_pares.py` para unir pares de anos consecutivos e calcular a evasão anual (`evasao_YYYY_YYYY.csv`), salvando em `data/processed/`.  

2. **IBGE**  
   1. Colocar os arquivos XLS do IBGE em `data/raw/ibge_xls/`.  
   2. Executar `src/ibge/extracao.py` para extrair as planilhas e gerar CSVs intermediários em `data/interim/ibge_csv/`.  
   3. Executar `src/ibge/limpeza.py` para limpar e padronizar colunas conforme `src/ibge_colunas.py`, salvando as tabelas finais em `data/processed/ibge_csv_final/`.  

3. **Agregação e Integração**  
   1. Executar `src/uniao_inep_pares.py` para combinar todos os pares de anos de evasão (`evasao_YYYY_YYYY.csv`), calcular médias e evasões acumuladas ponderadas, e gerar arquivos agregados por município, UF e Brasil em `data/processed/`.  
   2. Executar `src/uniao_inep_ibge.py` para integrar os resultados agregados de evasão com os dados censitários do IBGE (`ibge_csv_final/`), produzindo versões finais completas (`municipios_evasao_valida_ibge_2020_2024.csv` e `municipios_evasao_invalida_ibge_2020_2024.csv`) em `data/processed/`.  


## Requisitos

- Python 3.11+
functools==0.5
numpy==2.3.4
pandas==2.3.3

Instalar dependências:

```bash
pip install -r requirements.txt

