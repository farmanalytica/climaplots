# -*- coding: utf-8 -*-
"""ClimaPlots service layer: pure computation, free of Qt widgets.

Modules:
    nasa_power_service  - NASA POWER data fetch
    indices_service     - ETCCDI climate indices + SPI
    stats_service       - Mann-Kendall / Pettitt title fragments
    plot_service        - plotly figure builders (returns PlotResult)
    orchestrator        - sequences fetch + indices into one ClimateData
    settings_manager    - QSettings persistence (proxy)
    types               - ClimateData / PlotResult dataclasses
"""
from . import (  # noqa: F401
    indices_service,
    nasa_power_service,
    orchestrator,
    plot_service,
    settings_manager,
    stats_service,
)
from .types import ClimateData, PlotResult  # noqa: F401
