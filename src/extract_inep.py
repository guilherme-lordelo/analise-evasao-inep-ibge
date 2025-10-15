import os
import pandas as pd

# === ENTRADA DO ANO ===
ano = input("Digite o ano do arquivo INEP a ser reduzido (ex: 2022): ").strip()
input_filename = f"MICRODADOS_CADASTRO_CURSOS_{ano}.CSV"

# === CAMINHOS DE ARQUIVO ===
RAW_DIR = os.path.join("data", "raw")
INTERIM_DIR = os.path.join("data", "interim")
INPUT_FILE = os.path.join(RAW_DIR, input_filename)
OUTPUT_FILE = os.path.join(INTERIM_DIR, f"inep_reduzido_{ano}.csv")
REMOVIDAS_FILE = os.path.join(INTERIM_DIR, f"inep_removidas_{ano}.csv")

# === VERIFICAÇÕES ===
if not os.path.exists(INPUT_FILE):
	print(f"Arquivo não encontrado: {INPUT_FILE}")
	print("Verifique se o nome do arquivo segue o padrão 'MICRODADOS_CADASTRO_CURSOS_XXXX.CSV'.")
	exit(1)

os.makedirs(INTERIM_DIR, exist_ok=True)

# === CONFIGURAÇÕES ===
ENCODING = "latin1"  # pode ser alterado para 'utf-8' se necessário
SEP = ";"  # separador padrão dos microdados do INEP

# === COLUNAS RELEVANTES ===
COLUNAS_SELECIONADAS = [
	"NU_ANO_CENSO",
	"SG_UF",
	"NO_MUNICIPIO",
	"CO_MUNICIPIO",
	"TP_REDE",
	"TP_MODALIDADE_ENSINO",
	"TP_GRAU_ACADEMICO",
	"TP_ORGANIZACAO_ACADEMICA",
	"IN_CAPITAL",
	"QT_ING_TOTAL",
	"QT_MAT_TOTAL",
	"QT_CONC_TOTAL",
	"QT_SIT_TRANCADA",
	"QT_SIT_DESVINCULADO",
	"QT_SIT_TRANSFERIDO",
	"QT_SIT_FALECIDO",
	"QT_ING_FEM",
	"QT_ING_MASC",
	"QT_MAT_FEM",
	"QT_MAT_MASC",
	"QT_ING_FINANC",
	"QT_MAT_FINANC",
	"QT_CONC_FINANC"
]

# === ETAPA 1: LER HEADER ===
print(f" Lendo cabeçalho de {input_filename}...")
with open(INPUT_FILE, "r", encoding=ENCODING) as f:
	header = f.readline().strip().split(SEP)

# Detectar nomes antigos de colunas (anos anteriores a 2024)
mapeamento_renome = {}
if "QT_ING" in header and "QT_ING_TOTAL" not in header:
	mapeamento_renome["QT_ING"] = "QT_ING_TOTAL"
if "QT_MAT" in header and "QT_MAT_TOTAL" not in header:
	mapeamento_renome["QT_MAT"] = "QT_MAT_TOTAL"
if "QT_CONC" in header and "QT_CONC_TOTAL" not in header:
	mapeamento_renome["QT_CONC"] = "QT_CONC_TOTAL"

# Ajustar colunas selecionadas considerando o mapeamento
colunas_existentes = []
for c in COLUNAS_SELECIONADAS:
	if c in header:
		colunas_existentes.append(c)
	elif c in mapeamento_renome.values() and list(mapeamento_renome.keys())[list(mapeamento_renome.values()).index(c)] in header:
		colunas_existentes.append(list(mapeamento_renome.keys())[list(mapeamento_renome.values()).index(c)])

# Avisar sobre colunas ausentes
faltando = set(COLUNAS_SELECIONADAS) - set([mapeamento_renome.get(c, c) for c in colunas_existentes])
if faltando:
	print(f" Atenção: as seguintes colunas não foram encontradas e serão ignoradas: {faltando}")

# Guardar o mapeamento para renomear depois da leitura
renomear_apos_leitura = mapeamento_renome

# === ETAPA 2: LEITURA PRINCIPAL ===
print(f" Lendo arquivo completo de {ano} ...")
df = pd.read_csv(
	INPUT_FILE,
	sep=SEP,
	usecols=colunas_existentes,
	encoding=ENCODING,
	low_memory=False
)

# Aplicar renomeação de colunas antigas, se necessário
df = df.rename(columns=renomear_apos_leitura)

# === ETAPA 3: LIMPEZA ===
print(" Limpando dados...")

# 3.1 — Linhas sem CO_MUNICIPIO
sem_municipio = df[df["CO_MUNICIPIO"].isna() | (df["CO_MUNICIPIO"].astype(str).str.strip() == "")]
print(f" Linhas sem código de município: {len(sem_municipio):,}")

# 3.2 — Salvar linhas removidas (somente as sem município)
if len(sem_municipio) > 0:
    sem_municipio.to_csv(REMOVIDAS_FILE, sep=";", index=False, encoding="utf-8")
    print(f" Linhas removidas salvas em: {REMOVIDAS_FILE}")

# 3.3 — Manter apenas válidas
df = df.dropna(subset=["CO_MUNICIPIO"], how="any")

# === ETAPA 4: SALVAR RESULTADO ===
df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8")
print(f" Arquivo reduzido salvo em: {OUTPUT_FILE}")
print(f" Total de linhas processadas: {len(df):,}")
