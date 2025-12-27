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
        - POP_TOTAL
        - PERC_URBANA
        - PERC_RURAL
        - PERC_HOMEM
        - PERC_MULHER
        - RAZAO_SEXO

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

A etapa de `transformação` realiza todas as mudanças estruturais dentro de planilhas.

O arquivo de configuração controla os seguintes aspectos da `Transformação`:

*   **Agrupamento de Colunas (`merges_colunas`):** Permite agrupar faixas de dados de forma declarativa.
    *   **fontes:** Colunas originais do CSV.
    *   **destino:** Nova coluna consolidada.
    *   **metodo:** Operação aplicada (ex: `soma`).

Exemplo:

        merges_colunas:
        - destino: PERC_0_A_24_RURAL
            fontes:
            - PERC_0_A_5_RURAL
            - PERC_6_A_14_RURAL
            - PERC_15_A_24_RURAL
            metodo: soma
*   **Transformação Logit (`transformacoes_logit`):** Aplica a transformação logit em variáveis de porcentagem.
    *   **fonte:** Coluna original
    *   **destino:** Nova coluna contendo o valor transformado em logit.
    *   **metodo:** Transformação matemática `logit(x) = ln(x / (1 - x))`.

Exemplo:

        transformacoes_colunas:

            - fonte: PERC_URBANA
            destino: PERC_URBANA_LOGIT
            tipo: logit
            escala_origem: "0-100"

            - fonte: PERC_HOMEM
            destino: PERC_HOMEM_LOGIT
            tipo: logit
            escala_origem: "0-100"


*   **Remoção:** O campo `remover_colunas` permite excluir colunas .

Exemplo:

        remover_colunas:
          - PERC_RURAL
          - PERC_MULHER
          - RAZAO_SEXO

Colunas usadas como base para transformações são automaticamente removidas e não precisam ser incluídas para remoção. O objetivo é não manter colunas redundantes no conjunto de análise final.

**Carga**

A etapa de `carga` une todas as planilhas transformadas e persiste o resultado em um arquivo único final.

O arquivo de configuração controla os seguintes aspectos da `Carga`:

*   **Definição do nome final** O usuário decide o nome do arquivo IBGE unido final.

## Requisitos

- Python 3.11+

# Instruções de Uso:


## Preparação do ambiente

### Clonar repositório
    git clone https://github.com/guilherme-lordelo/analise-evasao-inep-ibge.git
### Instalar projeto como pacote
    pip install -e .
### Posicionar arquivos brutos (disponíveis nos portais oficiais das instituições)

Manter os arquivos originais INEP em:

    data/RAW/inep_micros/
Manter os arquivos originais IBGE em:

    data/RAW/ibge_xls/
## Alinhar o comportamento do pipeline ao desejado através dos arquivos de configuração YAML
### Edição do arquivo de configuração INEP em:
    config/inep.yml
### Edição do arquivo de configuração IBGE em:
    config/ibge.yml
## Execução dos Pipelines

### Pipeline INEP

- Extração: `python -m brpipe.scripts.inep.executar_extracao`
- Transformação: `python -m brpipe.scripts.inep.executar_transformacao`

### Pipeline IBGE

- Extração: `python -m brpipe.scripts.ibge.executar_extracao`
- Transformação: `python -m brpipe.scripts.ibge.executar_transformacao`

