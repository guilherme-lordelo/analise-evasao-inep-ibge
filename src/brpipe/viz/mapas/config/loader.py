# src/brpipe/viz/mapas/config/loader.py

from brpipe.utils.config import load_config
from .colunas_config import (
    ColunasConfig,
    TerritoriaisConfig,
    MunicipioColunasConfig,
    UFColunasConfig,
)
from brpipe.utils.config import load_config
from .plot_config import PlotConfig
from .mapas_config import MapaConfig
from .dados_config import *

_CFG = load_config("mapas")

def carregar_dados() -> DadosConfig:
    dados = _CFG["dados"]
    metrica = dados["metricas"]["principal"]
    arquivos = dados["arquivos"]

    return DadosConfig(
        formato=dados["formato"],
        separador=dados.get("separador", ";"),
        arquivos=ArquivosDadosConfig(
            municipio=arquivos["municipio"],
            uf=arquivos["uf"],
            nacional=arquivos.get("nacional", {}),
        ),
        metrica_principal=MetricaConfig(
            coluna_mapa=metrica["coluna_mapa"],
            wide=MetricaWideConfig(**metrica["wide"]) if "wide" in metrica else None,
            long=MetricaLongConfig(**metrica["long"]) if "long" in metrica else None,
        ),
    )


def carregar_colunas() -> ColunasConfig:
    territoriais = _CFG["colunas"]["territoriais"]
    municipio = territoriais["municipio"]

    return ColunasConfig(
        territoriais=TerritoriaisConfig(
            municipio=MunicipioColunasConfig(
                malha=municipio["malha"],
                tabela=municipio["tabela"],
                uf=municipio["uf"],
            ),
            uf=UFColunasConfig(
                malha=territoriais["uf"]["malha"],
                tabela=territoriais["uf"]["tabela"],
            )
            
        )
    )

def carregar_plot() -> PlotConfig:
    plot = _CFG["plot"]

    return PlotConfig(
        cmap=plot["cmap"],
        legend_shrink=plot["legend_shrink"],
    )

def _carregar_mapa(chave: str) -> MapaConfig:
    cfg = _CFG[chave]

    return MapaConfig(
        figsize=tuple(cfg["figsize"]),
        legend_label=cfg["legend_label"],
    )

def carregar_municipios() -> MapaConfig:
    return _carregar_mapa("municipios")

def carregar_uf() -> MapaConfig:
    return _carregar_mapa("uf")