import os
import pandas as pd

# === CONFIGURAÇÕES ===
INPUT_FILE = os.path.join("data", "raw", "MICRODADOS_CADASTRO_CURSOS_2024.CSV")
OUTPUT_FILE = os.path.join("data", "processed", "inep_reduzido.csv")
ENCODING = "latin1"  # pode ser alterado para 'utf-8' se necessário
SEP = ";"  # separador padrão dos microdados do INEP

# === COLUNAS RELEVANTES ===
COLUNAS_SELECIONADAS = [
	"NU_ANO_CENSO",
	"NO_REGIAO",
	"SG_UF",
	"NO_MUNICIPIO",
	"CO_MUNICIPIO",
	"CO_IES",
	"NO_CURSO",
	"TP_REDE",
	"TP_MODALIDADE_ENSINO",
	"TP_GRAU_ACADEMICO",
	"QT_ING_TOTAL",
	"QT_MAT_TOTAL",
	"QT_CONC_TOTAL",
	"QT_SIT_TRANCADA",
	"QT_SIT_DESVINCULADO",
	"QT_SIT_TRANSFERIDO",
	"QT_SIT_FALECIDO"
]

# === ETAPA 1: LER O HEADER ===
with open(INPUT_FILE, "r", encoding=ENCODING) as f:
	header = f.readline().strip().split(SEP)

# Verificar se todas as colunas selecionadas estão no arquivo
colunas_existentes = [c for c in COLUNAS_SELECIONADAS if c in header]
faltando = set(COLUNAS_SELECIONADAS) - set(colunas_existentes)
if faltando:
	print(f"Atenção: as seguintes colunas não foram encontradas e serão ignoradas: {faltando}")

# === ETAPA 2: LER SOMENTE AS LINHAS A PARTIR DA 11780 ===
print("🔍 Lendo arquivo a partir da linha 11780...")
df = pd.read_csv(
	INPUT_FILE,
	sep=SEP,
	skiprows=range(1, 11779),  # pula linhas 2 até 11780 (header é mantido)
	usecols=colunas_existentes,
	encoding=ENCODING,
	low_memory=False
)

# === ETAPA 3: LIMPEZA BÁSICA ===
# Remove linhas sem município ou curso
df = df.dropna(subset=["CO_MUNICIPIO", "NO_CURSO"], how="any")

# Remove duplicatas se houver
df = df.drop_duplicates()

# === ETAPA 4: SALVAR RESULTADO ===
df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8")
print(f"Arquivo salvo com sucesso: {OUTPUT_FILE}")
print(f"Total de linhas processadas: {len(df)}")
