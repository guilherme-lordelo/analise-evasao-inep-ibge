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


# Configurações do Pipeline (YAML)

O comportamento do pipeline é definido pelos arquivos de configuração, permitindo ajustes em cálculos e estruturas sem alterar o código-fonte.

## Configuração INEP (`inep.yml`)

Gerencia os Microdados do Censo da Educação Superior.

**Extração**

Refere-se à etapa de leitura dos arquivos INEP originais. Na implementação atual, são persistidas versões intermediárias dos dados no diretório `/INTERIM`. Além disso, operações que reduzem o volume de dados são realizadas nessa etapa ao invés de aconterem na `Transformação` com o fim de preservar espaço em disco e memória RAM.

O arquivo de configuração controla os seguintes aspectos da `Extração`:
*   **Definição de nomes de arquivos de entrada e saída:** Atualmente, o usuário define por configuração o nome dos arquivos brutos INEP, omitindo o ano de referência. Também define o nome de arquivos de saídas intermediários salvos em `/INTERIM`.
*   **Definição de colunas (variáveis) operacionais:** Os microdados INEP possuem um grande número de colunas. Somente aquelas explicitamente declaradas na configuração serão mantidas.
*   **Mapeamento de Cabeçalhos:** O campo `mapeamento_colunas` normaliza divergências de nomes entre diferentes anos do Censo.
*   **Filtro por categoria:** Função de remoção de registros com valor de coluna categórica definido. Permite trabalhar com um subconjunto dos dados. Exemplo:

        TP_MODALIDADE_ENSINO:
            descricao: "Modalidade de ensino"
            valores:
                1: "Presencial"
                2: "Educação a Distância"
            filtro_excluir:
                - 2
    Remove cursos EaD do conjunto de dados.
*   **Tratamento de registros sem código municipal:** O usuário pode decidir por descartar ou manter linhas sem código municipal. São uma minoria de cursos EaD não associados à região específica alguma. Se mantidos, serão atribuídos nomes municipal e estadual para esses cursos, também definidos por configuração.

**Transformação**

Os microdados INEP, atualmente, trabalham com nível de agregação por curso. Esse projeto, por outro lado, trabalha com nível mínimo municipal. Logo, a transformação deve agregar os dados originais. O pipeline permite níveis municipal, estadual e nacional de agregação.

A etapa de transformação também é responsável pelo cálculo de métricas definidas pelo usuário como a evasão operacional. As fórmulas são calculadas para cada nível de agregação.

O arquivo de configuração controla os seguintes aspectos da `Transformação`: 

*   **Peso:** `coluna_peso_inep` Define qual variável quantitativa será utilizada como base numérica nas agregações condicionadas por variáveis categóricas. Exemplo:
    `TP_REDE` define se a rede é pública ou privada.
    Se `QT_MAT_TOTAL` for selecionada como coluna de peso, as agregações calcularão distribuição percentual de alunos matriculados em cada tipo de rede.
    Nesse processo, a variável categórica é desdobrada em colunas derivadas, uma para cada valor possível da categoria definido no YAML.
*   **Fórmulas Definidas pelo Usuário:** Utiliza `{p}` (ano base) e `{n}` (ano seguinte).
    *   *Exemplo:* `expressao: "1 - ((QT_MAT_FINANC_{n} - QT_ING_FINANC_{n}) / (QT_MAT_FINANC_{p} - QT_CONC_FINANC_{p}))"` calcula a evasão anual considerando apenas estudantes com financiamento.
*   **Regras de Validação:** Filtros opcionais definidos pelo usuário associados a alguma fórmula, servindo para validar ou invalidar as mesmas.
    *   *Exemplo:* `regra: "(QT_MAT_FINANC_{n} - QT_ING_FINANC_{n}) > 0"` define que a evasão anual de financiados somente é válida se o número de matriculados no ano seguinte é maior que o número de ingressantes no ano seguinte.

**Carga**

Persiste o arquivo final resultante das operações de `Transformação`.

O arquivo de configuração controla os seguintes aspectos da `Carga`: 
*   **Formato do arquivo CSV persistido:** define caractere de separação, codificação e ordem de colunas.


## Configuração IBGE (`ibge.yml`)

Gerencia os dados demográficos IBGE. Consiste primariamente de um dicionário de dados contendo uma representação da estrutura das tabelas IBGE usadas, incluindo as `Sheets` (planilhas) que constituem cada arquivo `xls`.

Os cabeçalhos das panilhas IBGE são compostos por mais de uma linha, e fazem uso de mesclagem de células. Durante a conversão de `xls` para `csv`, esses cabeçalhos perdem o sentido, fato que implica na necessidade de conceber um dicionário semântico.

Nesse contexto, o arquivo de configuração IBGE provê nomes de arquivos, planilhas e novos nomes para colunas, além de orientar o código sobre quais colunas devem sofrer transformações ou serem descartadas.

**Extração**

A etapa de `extração` lê arquivos no formato `xls`, extrai todas as planilhas dentro desses arquivos e persiste versões intermediárias em `/INTERIM`.

O arquivo de configuração controla os seguintes aspectos da `Extração`: 

*   **Definição da estrutura de entrada e de saída:** Organiza e modela as planilhas para uso na extração e transformação. Exemplo:
  ```yaml
    tab2: # Nome do arquivo de entrada
        descricao_tabela: "População residente por faixas etárias, com detalhamento total, urbano e rural."
        sheets:
          - sheet_id: A # Primeira planilha do arquivo
            descricao_sheet: "Totais gerais de população por faixas etárias."
            arquivo: "tab2_faixas_etarias_total.csv" # Nome de saída da primeira planilha
            colunas: # Novos nomes de colunas
                - POP_RESIDENTE_TOTAL
                - PERC_0_A_5
                - PERC_6_A_14
                - PERC_15_A_24
                - PERC_25_A_39
                - PERC_40_A_59
                - PERC_60_OU_MAIS

          - sheet_id: B # Segunda planilha do arquivo
            descricao_sheet: "População urbana por faixas etárias."
            arquivo: "tab2_faixas_etarias_urbana.csv" # Nome de saída da segunda planilha
            colunas: # Novos nomes de colunas
                - POP_RESIDENTE_URBANA
                - PERC_0_A_5_URBANA
                - PERC_6_A_14_URBANA
                - PERC_15_A_24_URBANA
                - PERC_25_A_39_URBANA
                - PERC_40_A_59_URBANA
                - PERC_60_OU_MAIS_URBANA

          - sheet_id: C # Terceira planilha do arquivo
            descricao_sheet: "População rural por faixas etárias."
            arquivo: "tab2_faixas_etarias_rural.csv" # Nome de saída da terceira planilha
            colunas: # Novos nomes de colunas
                - POP_RESIDENTE_RURAL
                - PERC_0_A_5_RURAL
                - PERC_6_A_14_RURAL
                - PERC_15_A_24_RURAL
                - PERC_25_A_39_RURAL
                - PERC_40_A_59_RURAL
                - PERC_60_OU_MAIS_RURAL
```

**Transformação**

A etapa de `transformação` realiza todas as mudanças estruturais nas de planilhas, incluindo agrupamentos de coluna, agrupamentos de registro por estado e nacional, bem como definição de tipos de dado para gráficos.

O arquivo de configuração controla os seguintes aspectos da `Transformação`:

*   **Definição das colunas de peso:** Determina quais as colunas que podem ser usadas para ponderação. Essas colunas não podem ser usadas como fonte de agrupamento de coluna e não podem ser removidas.

Exemplo:

    colunas_peso:
    populacao: POP_TOTAL
    unidades: UNIDADES_DOMESTICAS_TOTAL
    domicilios: DOMICILIOS_TOTAL

*   **Definição de tipos:** Os campos `formato` e `coluna_peso` devem ser incluídos para caracterizar os tipos `PORCENTAGEM`, `MEDIA` e `PROPORCAO`. Enquanto que `CONTAGEM` é considerado campo padrão sem peso e dispensa declarações explicítas.

        colunas:
          - POP_TOTAL      # Usa padrão "CONTAGEM"
          - PERC_URBANA:   # "PROPORCAO" deve declarar formato e coluna de peso
              formato: PROPORCAO
              coluna_peso: populacao
Colunas usadas como fonte de agrupamento ou que serão removidas também dispensam declaração de formato.

*   **Agrupamento de Colunas (`merges_colunas`):** Permite agrupar faixas de dados de forma declarativa.
    *   **destino:** Nome da nova coluna.
    *   **fontes:** Índices das colunas originais do CSV.
    *   **metodo:** Define a lógica de agrupamento.
    *   **peso_merge:** Valor de cada índice para ponderação, um valor para cada coluna fonte.
    *   **formato:** Define o o tipo de dado para posterior agregação e análises.
    *   **coluna_peso:** Define a coluna peso usada no agrupamento de colunas e no agrupamento de registro por estado e nacional.

Exemplo:

        merges_colunas:
          - destino: IDADE_MEDIA_ESTIMADA
            fontes_idx: [2, 3, 4, 5, 6, 7]
            metodo: MEDIA_PONDERADA
            peso_merge: [2.5, 10, 19.5, 32, 49.5, 70]
            formato: MEDIA
            coluna_peso: "populacao"

*   **Remoção:** O campo `remover_colunas` permite excluir colunas por índice.

Exemplo:

        remover_colunas_idx:
          - 1


Colunas usadas como base para transformações são automaticamente removidas e não precisam ser incluídas para remoção.

**Carga**

A etapa de `carga` une todas as planilhas transformadas e persiste o resultado em um arquivo único final.

O arquivo de configuração controla os seguintes aspectos da `Carga`:

*   **Definição do nome final** O usuário decide o nome do arquivo IBGE unido final nos níveis municipal, estadual e nacional.

Exemplo:

    arquivo_final_municipios: "ibge_final_municipios.csv"
    arquivo_final_estados: "ibge_final_estados.csv"
    arquivo_final_nacional: "ibge_final_nacional.csv"

## Requisitos

- Python 3.11+

# Instruções de Uso:


## Preparação do ambiente

### Clonar repositório
    git clone https://github.com/guilherme-lordelo/analise-evasao-inep-ibge.git

### Instalação em Ambiênte virtual (Recomendado):
    python -m venv venv

    .\venv\Scripts\activate

### Instalar projeto como pacote
    pip install -e .
### Posicionar arquivos brutos (disponíveis nos portais oficiais das instituições)

Posicionar os arquivos originais INEP em:

    data/RAW/INEP/
Posicionar os arquivos originais IBGE em:

    data/RAW/IBGE/
Posicionar as malhas territóriais em:
    /DATA/SHAPEFILES/BR_Municipios_202
    /DATA/SHAPEFILES/BR_UF_2024


### Inicialização da Interface Gráfica para Alinhamento do Comportamento

    streamlit run src/ui/app.py

## Execução dos Pipelines e Criação de Visualizações

### Pipeline INEP

- Extração: `python -m brpipe.scripts.inep.executar_extracao`
- Transformação: `python -m brpipe.scripts.inep.executar_transformacao`

### Pipeline IBGE

- Extração: `python -m brpipe.scripts.ibge.executar_extracao`
- Transformação: `python -m brpipe.scripts.ibge.executar_transformacao`

### Visualizações

- Linhas Temporais: `python -m brpipe.scripts.viz.gerar_linha_temporal`
- Gráficos de Dispersão: `python -m brpipe.scripts.viz.gerar_scatter`

