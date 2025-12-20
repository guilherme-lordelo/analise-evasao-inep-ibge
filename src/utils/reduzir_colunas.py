import pandas as pd
from typing import List, Optional

from inep.config import VARIAVEIS_CONFIG


def reduzir_colunas(
    df: pd.DataFrame,
    variaveis: List[str],
    ano: Optional[str] = None,
    manter_peso: bool = False,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Remove colunas do df correspondentes às variáveis fornecidas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    variaveis : List[str]
        Lista de nomes base de variáveis (sem ano).
    ano : str, opcional
        Se fornecido, procura colunas no formato "{variavel}_{ano}".
        Se None, assume que o df contém exatamente as colunas em `variaveis`.
    manter_peso : bool, opcional
        Se True, não remove a coluna de peso (COLUNA_PESO) mesmo que esteja em `variaveis`.
    inplace : bool, opcional
        Se True, remove diretamente no df. Caso contrário, retorna cópia reduzida.

    Retorna
    -------
    pd.DataFrame
        O DataFrame reduzido, contendo apenas as colunas que não foram removidas.
    """

    if manter_peso:
        variaveis = [v for v in variaveis if v != VARIAVEIS_CONFIG.coluna_peso]

    if ano is None:
        # O nome da coluna deve coincidir exatamente com os nomes dados
        colunas_remover = [v for v in variaveis if v in df.columns]
    else:
        # Aplicar padrão {variavel}_{ano}
        colunas_remover = [f"{v}_{ano}" for v in variaveis if f"{v}_{ano}" in df.columns]

    if inplace:
        df.drop(columns=colunas_remover, inplace=True, errors="ignore")
        return df
    else:
        return df.drop(columns=colunas_remover, errors="ignore")
