# Projeto TCC - Educação Superior e Evasão

Este projeto tem como objetivo analisar a evasão na educação superior brasileira,
a partir dos microdados do Censo da Educação Superior (INEP, 2024),
relacionando-os futuramente com indicadores socioeconômicos municipais (IBGE).

## Estrutura de diretórios
- `data/raw/` → dados brutos originais, não modificados (não versionados no GitHub).
- `data/interim/` → dados parcialmente processados.
- `data/processed/` → dados finais prontos para análise.
- `src/` → scripts de processamento.
- `notebooks/` → notebooks exploratórios.

## Fluxo de Processamento
1. Colocar o arquivo bruto do INEP em `data/raw/`.
2. Executar `src/extract_inep.py` para gerar dataset reduzido (`inep_reduced.csv`) em `data/processed/`.
3. Executar `src/extract_ies.py` para gerar dataset de instituições (`inep_ies_reduced.csv`).
4. Executar `src/merge_ies_cursos.py` para consolidar cursos e IES em `inep_ies_merged.csv`.
5. (Próximo passo) Harmonizar e integrar as bases do IBGE com os dados do INEP.

## Requisitos
- Python 3.11+
- Pandas

Instalar dependências:
```bash
pip install -r requirements.txt
