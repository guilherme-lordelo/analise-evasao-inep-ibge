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

*   **Fórmulas Dinâmicas:** Utiliza `{p}` (ano base) e `{n}` (ano seguinte).
    *   *Exemplo:* `expressao: "QT_MAT_TOTAL_{n} - QT_MAT_TOTAL_{p}"` calcula a variação absoluta de matrículas.
*   **Regras de Validação:** Filtros opcionais definidos pelo usuário associados a alguma fórmula, servindo para validar ou invalidar as mesmas.
*   **Mapeamento de Cabeçalhos:** O campo `mapeamento_colunas` normaliza divergências de nomes entre diferentes anos do Censo.
*   **Peso:** `coluna_peso_inep` Define qual variável quantitativa será utilizada como base numérica nas agregações condicionadas por variáveis categóricas. Exemplo:
    `TP_REDE` define se a rede é pública ou privada.
    Se `QT_MAT_TOTAL` for selecionada como coluna de peso, as agregações calcularão distribuição percentual de alunos matriculados em cada tipo de rede.
    Nesse processo, a variável categórica é desdobrada em colunas derivadas, uma para cada valor possível da categoria definido no YAML.

## Configuração IBGE (`ibge.yml`)

Gerencia dados demográficos e estruturação de tabelas de população.

*   **Transformação de Colunas (`merges_colunas`):** Permite agrupar faixas de dados de forma declarativa.
    *   **fontes:** Colunas originais do CSV.
    *   **destino:** Nova coluna consolidada.
    *   **metodo:** Operação aplicada (ex: `soma`).
*   **Transformação Logit (`transformacoes_logit`):** Aplica a transformação logit em variáveis de porcentagem.
    *   **fonte:** Coluna original
    *   **destino:** Nova coluna contendo o valor transformado em logit.
    *   **metodo:** Transformação matemática `logit(x) = ln(x / (1 - x))`.

*   **Remoção:** O campo `remover_colunas` permite excluir variáveis indesejadas.

Colunas usadas como base para transformações são automaticamente removidas e não precisam ser incluídas para remoção. O objetivo é não manter colunas redundantes no conjunto de análise final.

## Regras de Customização

1.  **Consistência de Nomes:** Ao criar fórmulas, use apenas colunas listadas em `variaveis: quantitativas`.
2.  **Arquivos de Entrada:** Os prefixos em `arquivos: extracao` devem coincidir exatamente com o início dos nomes dos arquivos `.CSV` locais.
3.  **Encodings:** O padrão configurado é entrada em `latin1` (padrão governo) e saída em `utf-8` por padrão.
4.  **Agregação:** O pipeline gera automaticamente saídas nos níveis `municipios`, `estados` e `nacional` conforme definido na seção `transformacao`.



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

