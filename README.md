# Projeto - Integração e Visualização de Dados do INEP e IBGE: um Pipeline para Análise da Evasão no Ensino Superior

Este projeto tem como objetivo analisar a evasão na educação superior brasileira, a partir dos microdados do Censo da Educação Superior (INEP), relacionando-os com indicadores socioeconômicos municipais (IBGE).

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

- `src/brpipe/inep/` → Lógica de processamento dos dados do INEP.
- `src/brpipe/ibge/` → Lógica de processamento dos dados do IBGE.
- `src/brpipe/utils/` → Funções de apoio (leitura/escrita de arquivos, definição de caminhos).
- `src/brpipe/scripts/` → *Entry points* (pontos de entrada) para executar os pipelines.
- `src/brpipe/viz/` → Lógica de visualização (charts, dashboards, mapas).



## Requisitos

- Python 3.11+

Instalar dependências:

```bash
pip install -e .

## Execução dos Pipelines

### Pipeline INEP

- Extração: `python -m brpipe.scripts.inep.executar_extracao`
- Transformação: `python -m brpipe.scripts.inep.executar_transformacao`

### Pipeline IBGE

- Extração: `python -m brpipe.scripts.ibge.executar_extracao`
- Transformação: `python -m brpipe.scripts.ibge.executar_transformacao`

